#!python
#
#  Copyright 2023 Machine Learning and Language Processing (MLLP) research group
#                 Universitat Politècnica de València (UPV)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import json
import sys
import pyaudio
import sounddevice as sd
import queue
import threading
import math
import argparse
from MLLPStreamingClient import MLLPStreamingClient

parser = argparse.ArgumentParser()
parser.add_argument('api_host', help="API server hostname or IP")
parser.add_argument('api_port', help="API server port")
parser.add_argument('s2t_system_id', help="S2T (ASR) system ID")
parser.add_argument('t2t_system_id', help="T2T (MT) system ID")
parser.add_argument('t2s_system_id', help="T2S (TTS) system ID")
parser.add_argument('t2s_language_code', help="T2S (TTS) language code")
parser.add_argument('-u', '--api-user', default=None, help="TLP API username")
parser.add_argument('-k', '--api-key', default=None, help="TLP API secret key")
parser.add_argument('-c', '--ssl-cert-file', default=None, help="API server SSL .crt file")
parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug mode")

args = parser.parse_args()

cli = MLLPStreamingClient(args.api_host, args.api_port, args.api_user, args.api_key, args.ssl_cert_file, args.debug)

T2S_BLOCKSIZE = 4096

print("Retrieving systems info...")

# Get synthetised audio sample rate
ret = cli.Text2SpeechInfo()
for syst in ret:
    if syst["id"] == args.t2s_system_id or syst["info"]["id"] == args.t2s_system_id:
        sr = syst["info"]["sample_rate"]

def myAudioStreamGenerator():
     CHUNK = 250
     FORMAT = pyaudio.paInt16
     CHANNELS = 1
     RATE = 16000
     RECORD_SECONDS = 3600
     p = pyaudio.PyAudio()
     stream = p.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)
     for i in range(0, int((RATE / CHUNK) * RECORD_SECONDS)):
         data = stream.read(CHUNK)
         yield data
     stream.stop_stream()
     stream.close()
     p.terminate()

blocksize = 4096
q = queue.Queue()
event = threading.Event()

def playback_callback(outdata, frames, t, status):
    assert not status
    try:
        data = q.get_nowait()
    except:
        data = b''
    if len(data) < len(outdata):
        outdata[:len(data)] = data
        outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
    else:
        outdata[:] = data

astream = sd.RawOutputStream(
            samplerate=sr,
            blocksize=int(blocksize/2),
            channels=1,
            dtype='int16',
            callback=playback_callback,
            finished_callback=event.set)

def process_response(audiodata):
    nblocks = math.ceil(len(audiodata)/blocksize)
    i = 0
    while i < nblocks:
        q.put(audiodata[i*blocksize:(i+1)*blocksize], block=True)
        i += 1

def wrapper(iterator):
     t=""
     for resp in iterator:
         yield resp
         if resp["final_text"] != "":
             t = "%s %s" % (t, resp["final_text"].strip())
             sys.stdout.write("\r%s" % t)
             sys.stdout.flush()
             if resp["eos"] == True:
                 sys.stdout.write("\n")
                 sys.stdout.flush()
                 t=""
         if resp["ongoing_text"] != "":
             sys.stdout.write("\r%s %s" % (t, resp["ongoing_text"].strip()))
     
speech_dubbing_pipe_stream = cli.Text2Speech(args.t2s_system_id, wrapper(cli.Text2Text(args.t2t_system_id, cli.Speech2Text(args.s2t_system_id, myAudioStreamGenerator))), args.t2s_language_code)

print("Dubbing...")

x = b''

with astream:
    for resp in speech_dubbing_pipe_stream:
        if "audio_data" in resp:
            x += resp["audio_data"]
            if len(x) >= blocksize or len(resp["audio_data"]) < T2S_BLOCKSIZE:
                process_response(x)
                x = b''
    event.wait()
    
    
