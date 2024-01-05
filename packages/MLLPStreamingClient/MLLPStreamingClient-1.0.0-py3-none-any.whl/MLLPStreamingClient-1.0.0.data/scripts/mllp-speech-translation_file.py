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
import argparse
from MLLPStreamingClient import MLLPStreamingClient

parser = argparse.ArgumentParser()
parser.add_argument('api_host', help="API server hostname or IP")
parser.add_argument('api_port', help="API server port")
parser.add_argument('s2t_system_id', help="S2T (ASR) system ID")
parser.add_argument('t2t_system_id', help="T2T (MT) system ID")
parser.add_argument('input_audio_file', help="Input audio file (pcm_s16le, mono, 16khz)")
parser.add_argument('-u', '--api-user', default=None, help="TLP API username")
parser.add_argument('-k', '--api-key', default=None, help="TLP API secret key")
parser.add_argument('-c', '--ssl-cert-file', default=None, help="API server SSL .crt file")
parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug mode")

args = parser.parse_args()

cli = MLLPStreamingClient(args.api_host, args.api_port, args.api_user, args.api_key, args.ssl_cert_file, args.debug)

def myAudioStreamIterator():
    with open(args.input_audio_file, "rb") as fd:
        data = fd.read(250)
        while data != b"":
            yield data
            data = fd.read(250)

print("Translating...")

t=""
for resp in cli.Text2Text(args.t2t_system_id, cli.Speech2Text(args.s2t_system_id, myAudioStreamIterator)):
     if resp["final_text"] != "":
         t = "%s" % resp["final_text"].strip()
         sys.stdout.write('\033[2K\033[1G')
         sys.stdout.write("%s" % t)
         sys.stdout.flush()
         if resp["eos"] == True:
             sys.stdout.write("\n")
             sys.stdout.flush()
             t=""
     if resp["ongoing_text"] != "":
         sys.stdout.write("\r%s %s" % (t, resp["ongoing_text"].strip()))

