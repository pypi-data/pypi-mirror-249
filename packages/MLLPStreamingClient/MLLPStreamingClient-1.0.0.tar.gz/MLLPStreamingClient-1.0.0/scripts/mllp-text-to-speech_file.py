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
import soundfile
import numpy as np
import argparse
from MLLPStreamingClient import MLLPStreamingClient

parser = argparse.ArgumentParser()
parser.add_argument('api_host', help="API server hostname or IP")
parser.add_argument('api_port', help="API server port")
parser.add_argument('t2s_system_id', help="T2S (TTS) system ID")
parser.add_argument('t2s_language_code', help="T2S (TTS) language code")
parser.add_argument('input_text_file', help="Input text file (one sentence per line)")
parser.add_argument('output_audio_file', help="Output audio file path")
parser.add_argument('-u', '--api-user', default=None, help="TLP API username")
parser.add_argument('-k', '--api-key', default=None, help="TLP API secret key")
parser.add_argument('-c', '--ssl-cert-file', default=None, help="API server SSL .crt file")
parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug mode")

args = parser.parse_args()

cli = MLLPStreamingClient(args.api_host, args.api_port, args.api_user, args.api_key, args.ssl_cert_file, args.debug)

def myTextIterator():
    with open(args.input_text_file) as fd:
        for s in fd:
            yield s.strip()

print("Retrieving systems info...")

# Get synthetised audio sample rate
ret = cli.Text2SpeechInfo()
for sys in ret:
    if sys["id"] == args.t2s_system_id or sys["info"]["id"] == args.t2s_system_id:
        sr = sys["info"]["sample_rate"]


print("Synthetising...")

adata = np.array([], dtype=np.int16)
for k in cli.Text2Speech(args.t2s_system_id, myTextIterator, args.t2s_language_code):
    if "audio_data" in k:
        adata = np.concatenate((adata, np.frombuffer(k["audio_data"], dtype=np.int16)))

print("Writting output at %s..." % args.output_audio_file)

soundfile.write(args.output_audio_file, adata, sr)

