#!/usr/bin/env python
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
import argparse
from MLLPStreamingClient import MLLPStreamingClient

parser = argparse.ArgumentParser()
parser.add_argument('api_host', help="API server hostname or IP")
parser.add_argument('api_port', help="API server port")
parser.add_argument('s2t_system_id', help="S2T (ASR) system ID")
parser.add_argument('-u', '--api-user', default=None, help="TLP API username")
parser.add_argument('-k', '--api-key', default=None, help="TLP API secret key")
parser.add_argument('-c', '--ssl-cert-file', default=None, help="API server SSL .crt file")
parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug mode")

args = parser.parse_args()

cli = MLLPStreamingClient(args.api_host, args.api_port, args.api_user, args.api_key, args.ssl_cert_file, args.debug)

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
     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
         data = stream.read(CHUNK)
         yield data
     stream.stop_stream()
     stream.close()
     p.terminate()


print("Transcribing...")

t=""
for resp in cli.Speech2Text(args.s2t_system_id, myAudioStreamGenerator):
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
         


