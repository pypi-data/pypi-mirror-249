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
import threading 
import argparse
from MLLPStreamingClient import MLLPStreamingClient

parser = argparse.ArgumentParser()
parser.add_argument('api_host', help="API server hostname or IP")
parser.add_argument('api_port', help="API server port")
parser.add_argument('t2t_system_id', help="T2T (MT) system ID")
parser.add_argument('-u', '--api-user', default=None, help="TLP API username")
parser.add_argument('-k', '--api-key', default=None, help="TLP API secret key")
parser.add_argument('-c', '--ssl-cert-file', default=None, help="API server SSL .crt file")
parser.add_argument('-d', '--debug', default=False, action="store_true", help="Debug mode")

args = parser.parse_args()

cli = MLLPStreamingClient(args.api_host, args.api_port, args.api_user, args.api_key, args.ssl_cert_file, args.debug)

sem = threading.Semaphore()

def myTextIterator():
    while True:
        sem.acquire()
        s = input("> Type input text: ")
        yield s

for resp in cli.Text2Text(args.t2t_system_id, myTextIterator):
    print("   >> Output: %s" % resp["final_text"])
    sem.release()


