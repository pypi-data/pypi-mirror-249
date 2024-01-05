#  Copyright 2022 the MLLP-VRAIN research grup
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

"""
# The MLLP-TTP gRPC Streaming API client Python3 module

The [MLLP-TTP](https://ttp.mllp.upv.es/) gRPC Streaming API Python3 client
module implements a client library of the [MLLP-TTP gRPC Streaming
API](https://ttp.mllp.upv.es/mllp-streaming-api), based on the gRPC protocol.
Both have been developed by the [Machine Learning and Language
Processing](https://mllp.upv.es/) (MLLP) research group of the [Valencian
Research Institute on Artificial Intelligence](https://vrain.upv.es/),
[Universitat Politècnica de València](https://www.upv.es/). 

This module allows to develop your own streaming speech or text processing
application/backend. In particular, it offers several methods to perform
streaming Automatic Speech Recognition (ASR), streaming Speech Translation
(ST), streaming Speech Dubbing (SD), simultaneous Machine Translation (MT), and
incremental Text-To-Speech (TTS). This is done by properly using and combining
the three primitive rpc methods/endpoints offered by the API, *Speech2Text*,
*Text2Text* and *Text2Speech*, than can be directly called using this module.

In addition, the wheel package ships several Python3 scripts that illustrate
the usage of this Python3 module. These are:

- `mllp-speech-to-text_file.py`
- `mllp-speech-to-text_mic.py`
- `mllp-speech-translation_file.py`
- `mllp-speech-translation_mic.py`
- `mllp-speech-dubbing_file.py` (requires numpy)
- `mllp-speech-dubbing_mic.py`
- `mllp-text-to-speech_file.py` (requires numpy)
- `mllp-text-to-speech_terminal.py` (requires numpy)
- `mllp-text-to-text_file.py`
- `mllp-text-to-text_terminal.py`

Note that these scripts' installation directory is added to the PATH environment variable. 

## Installation

Via Pypi.org: 

```bash
pip install MLLPStreamingClient 
```

Via a provided .whl file: 

```bash
pip install MLLPStreamingClient_mllp-${VERSION}-py3-none-any.whl 
```

## Getting started

First, we have to import the `MLLPStreamingClient` library and create a `MLLPStreamingClient` class instance:

```python
from MLLPStreamingClient import MLLPStreamingClient
cli = MLLPStreamingClient(server_hostname, server_port, api_user, 
                          api_secret, server_ssl_cert_file)
```

_server_hostname_, _server_port_, _api_user_, _api_secret_ and _server_ssl_cert_file_ values can be retrieved 
from [TTP's API section](https://ttp.mllp.upv.es/index.php?page=api).

Next, and optionally, we can perform a explicit call to the rpc GetAuthToken method, to get a valid auth token
for the nextcoming rpc calls:

```python
 cli.AuthToken()
```

Please note that if we do not perform explicitly this call, it will be performed automatically by the library, when needed.

## Primitives 

### Speech2Text (S2T)

To check out the available Speech2Text (S2T) systems offered by the service, call the Speech2TextInfo rpc method:

```python
 systems = cli.Speech2TextInfo()
 import json
 print(json.dumps(systems, indent=4))
```

Then, we pick up our preferred S2T system (`system_id`), and start transcribing
our live audio stream supplied as an iterator or generator function called i.e.
`myStreamIterator()`, using the `Speech2Text()` class method.  This code block shows how to print consolidated
transcription chunks (`resp["final_text"]`) combined with non-consolidated,
ongoing ones (`resp["ongoing_text"]`). 

```python
for resp in cli.Speech2Text(system_id, myStreamIterator):
     if resp["final_text"] != "":
         t = "%s %s" % (t, resp["final_text"].strip())
         sys.stdout.write("\\r%s" % t)
         sys.stdout.flush()
         if resp["eos"] == True:
             sys.stdout.write("\\n")
             sys.stdout.flush()
             t=""
     if resp["ongoing_text"] != "":
         sys.stdout.write("\\r%s %s" % (t, resp["ongoing_text"].strip()))
```

Please note that consolidated transcription chunks are delivered with far more
delay than non-consolidated, ongoing (live) ones. However, these latter chunks
grow and change as new incoming audio data is processed, until the system
decides to consolidate. Please note that `resp["eos"]` is set to `True` when
the system outputs a consolidated end-of-sentence (eos) chunk. 

Audio data delivered *(yielded)* by the *myStreamIterator* function/iterator
must be compilant with the following specifications: PCM, single channel, 16khz
sample rate, 16bit little endian.  If your audio file or stream does not comply
with these specs, you should consider to transform it before delivering it to
the service, i.e.  by using [pydub.AudioSegment](http://pydub.com/), or using
external tools like `ffmpeg`.  A typical `ffmpeg` commandline call that would
convert any media file into an audio file compiling the aforementioned
specifications is:

```bash
ffmpeg -i $INPUT_MEDIA -ac 1 -ar 16000 -acodec pcm_s16le $OUTPUT_AUDIO.wav
```

Hence, we can implement a basic `myStreamIterator` function, that reads a
compilant wav file from disk, to test the service: 

```python
def myStreamIterator():
    with open(test_wav_file, "rb") as fd:
        data = fd.read(250)
        while data != b"":
            yield data
            data = fd.read(250)

for resp in cli.Speech2Text(system_id, myStreamIterator):
    ...
```

If you want to perform a more realistic test, you can try capture and stream your
own voice using a microphone and the [pyAudio](http://people.csail.mit.edu/hubert/pyaudio/) module:

```python
import pyaudio
def myStreamIterator():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 20
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
```
    
In adittion, two interesting features of the underlying S2T systems can be used
in your `myStreamIterator()` function. 

The first one is to **send the system an end-of-sentence (eos) signal**, thus
forcing the consolidation of the ongoing non-consolidated hypotheses. This can
be easily done by doing `yield None`, this is, sending an empty package. As
soon as the system processes an empty package, it will return a `resp['final_text']`
containing the latest consolidated text chunk, along with `resp['eos'] = True`.

The second one is **to inject any string into the audio stream**. The
S2T system will output that string unchanged and properly time-aligned with the
outcoming text stream. Just do, e.g. `yield "My Awesome Injected
String"`.  This feature can be useful e.g. in re-speaking scenarios for live TV
broadcasting, to insert on-place punctuation signs, speaker changes, HTML markup, etc.

### Text2Text (T2T)

To check out the available Text2Text (T2T) systems offered by the service, first we call
the Text2TextInfo rpc method:

```python
 systems = cli.Text2TextInfo()
 import json
 print(json.dumps(systems, indent=4))
```

Please note that T2T systems can be either Machine Translation (MT) systems
that translate text from a source to a target language, or monolingual text
postprocessing systems for adding casing, punctuation signs, markup, summarize,
etc.

Then, we pick up our preferred T2T system (`system_id`), and start converting 
our batch or live text stream, supplied as an iterator or generator function called i.e.
`myTextStreamIterator()`, using the `Text2Text()` class method.  


```python
for resp in cli.Text2Text(system_id, myTextIterator):
    print(resp["final_text"])
```

As in `Speech2Text()`, it also returns consolidated text chunks
(`resp["final_text"]`) combined with non-consolidated, ongoing ones
(`resp["ongoing_text"]`). This is to allow a direct, nested (piped) call of
both methods to build a custom cascaded Speech Translation application, so that
both consolidated and non-consolidated text chunks are translated. Indeed,
`Text2Text` rpc input message specification is identical to `Speech2Text()`
output rpc message specification. When using `Text2Text()` solely, output text is
delivered on the `"final_text"` field. 

Hence, we can implement a basic `myTextStreamIterator` function, that yields
some english sentences to be translated into another language: 

```python
def myTextStreamIterator():
    yield "We are pioneers and leaders in automatic speech recognition, machine translation, machine learning, natural language understanding and artificial intelligence.",
    yield "Through our advanced research in speech recognition, machine translation and artificial intelligence, we have solved many challenging problems improving human quality transcription, language understanding and translation accuracy.",
    yield "By converting spoken language into text, we make it easier to search, discover and analyze audio and video assets, significantly increasing their value.",

for resp in cli.Text2Text(system_id, myStreamIterator):
    ...
```

### Text2Speech (T2S)

To check out the available Text2Speech (T2S) systems offered by the service, first we call
the Text2SpeechInfo rpc method:

```python
 systems = cli.Text2SpeechInfo()
 import json
 print(json.dumps(systems, indent=4))
```

Then, we pick up our preferred T2S system (`system_id`), and we call the
`Text2Speech()` class method to start generating a stream of synthesized english
audio, from an input text stream, supplied as an iterator or generator function
called i.e.  `myTextStreamIterator()`.  

```python
import numpy as np
import soundfile as sf

sample_rate = 24000 # note: this is T2S system dependent
language = "en-us"
adata = np.array([], dtype=np.int16)
for resp in cli.Text2Speech(system_id, 
                            myTextStreamIterator, 
                            language):
    if "audio_data" in resp:
        adata = np.concatenate((adata, 
                                np.frombuffer(resp["audio_data"], 
                                dtype=np.int16)))
sf.write(f"output.wav", adata, sample_rate)

```

To test the service, we can use the `myTextStreamIterator()` function defined previously for *Text2Text*. 

## Advanced applications

### Speech Translation

We can build our custom Speech Translation application, by pipeing (nesting)
`Speech2Text()` and `Text2Text()` method calls, after having selected the
desired S2T and T2T systems, and using `myAudioStreamIterator` as an iterator
or generator method providing a continuous stream of audio data:

```python
for resp in cli.Text2Text(
                  t2t_system_id, 
                  cli.Speech2Text(
                        s2t_system_id, 
                        myAudioStreamIterator)):
    ....
```

### Speech Dubbing

We can build our custom Speech Dubbing application, by pipeing (nesting)
`Speech2Text()`, `Text2Text()` and `Text2Speech()` method calls, after having selected the
desired S2T, T2T, and T2S systems, and using `myAudioStreamIterator` as an iterator
or generator method providing a continuous stream of audio data:

```python
for resp in cli.Text2Speech(
                  t2s_system_id, 
                  cli.Text2Text(
                        t2t_system_id, 
                        cli.Speech2Text(
                              s2t_system_id, 
                              myAudioStreamIterator)), 
                  "en-us"):
    ....
```




"""

__all__ = ["MLLPStreamingClient"]

import sys
import grpc
import google.protobuf.empty_pb2 as empty_pb2
import google.protobuf.json_format as json_format
import logging
import traceback
from datetime import datetime
import MLLPStreamingClient.mllp_streaming_pb2_grpc as mllp_streaming_pb2_grpc
import MLLPStreamingClient.mllp_streaming_pb2 as mllp_streaming_pb2


class UnknownSystemException(Exception):
    """Raised when a provided system ID (string) does not exist"""
    pass

class NoSlotsAvailableException(Exception):
    """Raised when the requested system has no processing slots available"""
    pass

class MLLPStreamingClient():


    _SIGNATURE_HEADER_KEY = 'x-mllp-auth-token'

    def __init__(self, server_name, server_port, api_user=None, api_secret_key=None, server_cert_file=None, debug=False):
        """
        Creates a MLLPStreamingClient instance. 
    
        Parameters:
       
        - **_server_name_**: gRPC API server hostname or IP address.
        - **_server_port_**: gRPC API server port.
        - **_api_user_**: TTP API username (optional, if server does not require user auth).
        - **_api_secret_key_**: TTP API user secret key (optional, if server does not require user auth).
        - **_server_cert_file_** (optional): use SSL encryption, by providing an SSL certificate file of the gRPC API server.
        - **_debug_** (optional): enable/disable debug mode.
        """
        self._hostname = server_name
        self._port = server_port
        self._api_user = api_user
        self._api_secret = api_secret_key
        if server_cert_file != None:
            with open(server_cert_file, 'rb') as fd:
                self._server_cert = fd.read()
            self._ssl_credentials = grpc.ssl_channel_credentials(root_certificates=self._server_cert)
        else:
            self._server_cert = None
            self._ssl_credentials = None
        self._auth_token = None
        self._auth_token_expires = None
        self._credentials = None
        self.__create_logger(debug)
  
    def __create_logger(self, debug):
        """
        Init logger.
        """
        self._logger = logging.getLogger("MLLP Streaming Client")
        ch = logging.StreamHandler()
        if debug:
            self._logger.setLevel(logging.DEBUG)
            ch.setLevel(logging.DEBUG)
        else:
            self._logger.setLevel(logging.INFO)
            ch.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)
 
    def __dd(self, msg):
        self._logger.debug(msg);

    def __ii(self, msg):
        self._logger.info(msg);

    def __ww(self, msg):
        self._logger.warning(msg);

    def __ee(self, msg):
        self._logger.error(msg);

    def __generateCredentials(self):
        """
        Sets up self._credentials for nextcoming gRPC calls.
        """
        self._credentials = grpc.metadata_call_credentials(
           MLLPStreamingClient._AuthGateway(self._auth_token), None)
        if self._ssl_credentials != None:
            self._credentials = grpc.composite_channel_credentials(
                self._ssl_credentials, self._credentials)

    def __isAuth(self):
        """
        Checks if the client has a valid authentication token
        """
        return self._auth_token != None and self._auth_token_expires > datetime.now().timestamp()

    def __createChannel(self):
        if self._server_cert != None:
            return grpc.secure_channel("%s:%s" % (self._hostname, self._port), self._credentials)
        else:
            return grpc.insecure_channel("%s:%s" % (self._hostname, self._port))

    def __toJson(self, response):
        """
        Converts gRPC message to JSON (python dictionary)
        """
        return json_format.MessageToDict(response, 
            including_default_value_fields=True, 
            use_integers_for_enums=True,
            preserving_proto_field_name=True)

    def __toS2TRequestGenerator(self, system_id, audio_stream_iterator):
        """
        Converts the provided audio stream to S2TRequest messages
        """
        iterator = audio_stream_iterator
        if callable(audio_stream_iterator): 
            # audio_stream_iterator is a generator function
            iterator = audio_stream_iterator()
        yield mllp_streaming_pb2.S2TRequest(system_id=system_id)
        for data in iterator:
            if type(data) == str:
                yield mllp_streaming_pb2.S2TRequest(token=data)
            else: # bytes
                yield mllp_streaming_pb2.S2TRequest(data=data)

    def __toT2TRequestGenerator(self, system_id, text_iterator):
        """
        Converts the provided text stream to T2TRequest messages
        """
        iterator = text_iterator
        if callable(text_iterator):
            # text_iterator is a generator function
            iterator = text_iterator()
        yield mllp_streaming_pb2.T2TRequest(system_id=system_id)
        for t in iterator:
            if isinstance(t, str):
                yield mllp_streaming_pb2.T2TRequest(
                           data=mllp_streaming_pb2.T2TInputPackage(
                                    ongoing_text=None,
                                    final_text=t,
                                    eos=True)
                          )
            elif isinstance(t, dict):
                if t.get('final_text', None) == None and t.get('ongoing_text', None) == None:
                    raise Exception("text_iterator() dicts must contain 'ongoing_text' or 'final_text' keys")
                yield mllp_streaming_pb2.T2TRequest(
                           data=mllp_streaming_pb2.T2TInputPackage(
                                    ongoing_text=t.get('ongoing_text', None),
                                    final_text=t.get('final_text', None),
                                    eos=t.get('eos', False))
                           )
            else:
                raise Exception("text_iterator() must provide a sequence of dict or str")

    def __toT2SRequestGenerator(self, system_id, text_iterator, lang_code, attrs={}):
        """
        Converts the provided text stream to T2SRequest messages
        """
        iterator = text_iterator
        if callable(text_iterator):
            # text_iterator is a generator function
            iterator = text_iterator()
        for t in iterator:
            input_pkg = mllp_streaming_pb2.T2SInputPackage()
            if isinstance(t, str):
                input_pkg.text = t
            elif isinstance(t, dict):
                if t.get('final_text', "").strip() == "":
                    continue # skip this message, wait for final_text data.
                input_pkg.text = t['final_text']
            else:
                raise Exception("text_iterator() must provide a sequence of dict or str")
            input_pkg.lang_code = lang_code
            for key in attrs:
                try:
                    setattr(input_pkg, key, attrs[key])
                except AttributeError as e:
                    self.__ww("%s. Ignoring..." % str(e))
            yield mllp_streaming_pb2.T2SRequest(system_id=system_id, data=input_pkg)

    def AuthToken(self):
        """
        Implements the gRPC AuthToken call, to get a valid auth token for nextcoming gRPC calls.
    
        Explicitly calls to AuthToken with the API user name and API user secret provided to the class constructor. 
        Auth token and its lifetime is saved in this instance for the nextcoming gRPC calls.
        
        Returns an AuthTokenResponse in JSON format (python dictionary).
    
        Raises Exception if the server returns an error code, typically when authentication fails.
        """ 
        if self._credentials == None:
            self.__generateCredentials()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            resp = stub.AuthToken(mllp_streaming_pb2.AuthTokenRequest(user=self._api_user, password=self._api_secret))
        self.__dd("(GetAuthToken)\n%s" % self.__toJson(resp))
        if resp.code == mllp_streaming_pb2.ReturnCode.ERR:
            msg = "(GetAuthToken): auth failed (server returned ReturnCode.ERR)"
            self.__ee(msg)
            raise Exception(msg)
        self._auth_token = resp.auth_token
        self._auth_token_expires = resp.expiry_date
        self.__generateCredentials() # generate credentials with the given auth token
        self.__dd("Authentication successful as user '%s' (expires on: %s)" % (self._api_user, datetime.fromtimestamp(self._auth_token_expires).strftime("%Y-%m-%d %H:%M:%S")))
        return self.__toJson(resp)
         

    def Speech2TextInfo(self):
        """
        Implements the gRPC Speech2TextInfo call, to get information about all available streaming speech-to-text (S2T) systems.
    
        Returns a list of S2TInfoResponse messages as python dicts. See Speech2TextInfo rpc API call documentation for more details. 
    
        This method automatically calls to AuthToken(), if the MLLPStreamingClient object does not store a valid auth token. 
        """

        if not(self.__isAuth()):
            self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            systems = []
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.Speech2TextInfo(empty_pb2.Empty(), metadata=metadata):
                self.__dd("(Speech2TextInfo)\n%s" % self.__toJson(resp))
                systems.append(self.__toJson(resp))
        return systems


    def Speech2Text(self, system_id, audio_stream_iterator):
        """
        Implements the gRPC Speech2Text method call, to convert a stream of raw audio samples into text using a streaming speech-to-text (S2T) system.
    
        Parameters:
       
        - **_system_id_**: S2T system identifier. It can be either a `str` value ('info'->'id' from Speech2TextInfo(); recommended), or an `int` value ('id' key from Speech2TextInfo()).
        - **_audio_stream_iterator_**: an iterator or generator function providing chunks of raw audio data (bytes) in the following format: single channel (mono), 16khz, signed 16bit little endian.
    
        This method is a generator of S2TResponse messages as python dicts, thus providing a continuous stream of output text for the incoming audio stream feeded by **_audio_stream_iterator_**. See Speech2Text rpc API call documentation for more details. 
    
        This method automatically calls to AuthToken(), if the MLLPStreamingClient object does not store a valid auth token.
        """

        if not(self.__isAuth()):
           self.AuthToken()

        ret = self.Speech2TextInfo()

        # Convert String ID to Integer ID
        if isinstance(system_id, str):
            system_id_int = None
            for sys in ret:
                if sys["info"]["id"] == system_id:
                    system_id_int = sys["id"]
            if system_id_int == None:
                raise UnknownSystemException("Unknown Speech2Text system ID '%s'" % system_id)
            system_id = system_id_int

        # Check if system has free slots
        found = False
        for sys in ret:
            if sys["id"] == system_id:
                found = True
                if sys["slots"] == 0:
                    raise NoSlotsAvailableException("Requested Speech2Text System has no slots available")
        if not(found):
            raise UnknownSystemException("Unknown Speech2Text system ID '%s'" % system_id)
            
        # Call Speech2Text    
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.Speech2Text(self.__toS2TRequestGenerator(system_id, audio_stream_iterator), metadata=metadata):
                self.__dd(self.__toJson(resp))
                yield self.__toJson(resp)


    def Text2TextInfo(self):
        """
        Implements the gRPC Text2TextInfo call, to get information about all available simultaneous text-to-text (T2T) systems (typically translation, but also text postprocessing systems).
    
        Returns a list of T2TInfoResponse messages as python dicts. See Text2TextInfo rpc API call documentation for more details. 
    
        This method automatically calls to AuthToken(), if the MLLPStreamingClient object does not store a valid auth token. 
        """

        if not(self.__isAuth()):
            self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            systems = []
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.Text2TextInfo(empty_pb2.Empty(), metadata=metadata):
                self.__dd("(Text2TextInfo)\n%s" % self.__toJson(resp))
                systems.append(self.__toJson(resp))
        return systems


    def Text2Text(self, system_id, text_iterator):
        """
        Implements the gRPC Text2Text method call, to convert a stream of text into text (typically translation from one language to another, but also text post-processing), using a simultaneous text-to-text (T2T) system.
    
        Parameters:
       
        - **_system_id_**: T2T system identifier. It can be either a `str` value ('info'->'id' from Text2TextInfo(); recommended), or an `int` value ('id' key from Text2TextInfo()).
        - **_text_iterator_**: an iterator or generator function providing chunks of (a stream of) input text data. It can be either *dict* objects, with the following key-values: `{'ongoing_text':<str>, 'final_text':<str>, 'eos':<bool>}`, or *str* (text) objects. *dict* objects mimick *S2TResponse* and *T2TRequest* message specifications; this facilitates building a custom streaming Speech Translation application by simply pipeing *Speech2Text()* and *Text2Text()* calls. On the other hand, received *str* objects are automatically converted to *dict* objects as `{'ongoing_text':None, 'final_text':<str>, 'eos':True}`.
    
        This method is a generator of T2TResponse messages as python dicts, thus providing as output a continuous stream of output text converted from the input text feeded by **_text_iterator_**. See Text2Text rpc API call documentation for more details. 
    
        This method automatically calls to AuthToken(), if the MLLPStreamingClient object does not store a valid auth token.
        """

        if not(self.__isAuth()):
           self.AuthToken()

        ret = self.Text2TextInfo()

        # Convert String ID to Integer ID
        if isinstance(system_id, str):
            system_id_int = None
            for sys in ret:
                if sys["info"]["id"] == system_id:
                    system_id_int = sys["id"]
            if system_id_int == None:
                raise UnknownSystemException("Unknown Text2Text system ID '%s'" % system_id)
            system_id = system_id_int

        # Check if system has free slots
        found = False
        for sys in ret:
            if sys["id"] == system_id:
                found = True
                if sys["slots"] == 0:
                    raise NoSlotsAvailableException("Requested Text2Text System has no slots available")
        if not(found):
            raise UnknownSystemException("Unknown Text2Text system ID '%s'" % system_id)
 
        # Call Text2Text
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.Text2Text(self.__toT2TRequestGenerator(system_id, text_iterator), metadata=metadata):
                self.__dd(self.__toJson(resp))
                yield self.__toJson(resp)


    def Text2SpeechInfo(self):
        """
        Implements the gRPC Text2SpeechInfo call, to get information about all available incremental text-to-speech (T2S) systems.
    
        Returns a list of T2SInfoResponse messages as python dicts. See Text2SpeechInfo rpc API call documentation for more details. 
    
        This method automatically calls to AuthToken(), if the MLLPStreamingClient object does not store a valid auth token. 
        """

        if not(self.__isAuth()):
            self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            systems = []
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.Text2SpeechInfo(empty_pb2.Empty(), metadata=metadata):
                self.__dd("(Text2SpeechInfo)\n%s" % self.__toJson(resp))
                systems.append(self.__toJson(resp))
        return systems


    def Text2Speech(self, system_id, text_iterator, lang_code, **kwargs):
        """
        Implements the gRPC Text2Speech method call, to convert a stream of input text into a stream of synthesized audio, using an incremental text-to-speech (T2S) system.
    
        Parameters:
       
        - **_system_id_**: T2S system identifier. It can be either a `str` value ('info'->'id' from Text2SpeechInfo(); recommended), or an `int` value ('id' key from Text2SpeechInfo()).
        - **_text_iterator_**: an iterator o generator function providing chunks of (a stream of) input text data. It can be either *dict* objects, with the following key-values: `{'ongoing_text':<str>, 'final_text':<str>, 'eos':<bool>}`, or *str* (text) objects. *dict* objects mimick *S2TResponse* and *T2TRequest* message specifications; this facilitates building a custom streaming Speech Dubbing application by simply pipeing *Speech2Text()*, *Text2Text()*, and *Text2Speech()* calls. 
        - **_lang_code_**: language code (ISO 639-1) for the synthesised speech. Must be supported by the T2S system (see Text2SpeechInfo).
        
        **_kwargs_** can be used to provide optional parameters allowed in the T2SInputPackage message (e.g. **_speaker_id_**, **_tempo_**, **_pitch_**, ...). 
    
        This method is a generator of T2SResponse gRPC messages as python dicts, providing a continuous stream of synthesized speech audio from the input text feeded by **_text_iterator_**. A dict containing the key "metadata", whose value is a T2SResponseMetadata rpc message encoded as a python dict, provides information about a particular chunk of synthesized speech audio (duration, sample rate, format, etc). This metadata message is always followed by many messages (python dicts) containing audio data (as bytes) for that audio chunk, under the key "audio_data" (as bytes). See Text2Speech rpc API call documentation for more details. 
    
        This method automatically calls to AuthToken(), if the MLLPStreamingClient object does not store a valid auth token.
        """

        attrs = {k:v for k,v in kwargs.items() if v}

        if not(self.__isAuth()):
           self.AuthToken()

        ret = self.Text2SpeechInfo()

        # Convert String ID to Integer ID
        if isinstance(system_id, str):
            system_id_int = None
            for sys in ret:
                if sys["info"]["id"] == system_id:
                    system_id_int = sys["id"]
            if system_id_int == None:
                raise UnknownSystemException("Unknown Text2Speech system ID '%s'" % system_id)
            system_id = system_id_int

        # Check if system has free slots
        found = False
        for sys in ret:
            if sys["id"] == system_id:
                found = True
                if sys["slots"] == 0:
                    raise NoSlotsAvailableException("Requested Text2Speech System has no slots available")
        if not(found):
            raise UnknownSystemException("Unknown Text2Speech system ID '%s'" % system_id)

        # Run Text2Speech 
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.Text2Speech(self.__toT2SRequestGenerator(system_id, text_iterator, lang_code, attrs), metadata=metadata):
                retd = self.__toJson(resp)
                # toJson serializes bytes to str base64-encoded; let's stick to bytes
                if resp.HasField("audio_data"):
                    retd["audio_data"] = resp.audio_data
                yield retd


    def AdminAddS2TNode(self, host, port):
        """
        Admin method: implements the gRPC AdminAddS2TNode call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            resp = stub.AdminAddS2TNode(mllp_streaming_pb2.AddNodeRequest(host=host, port=port), metadata=metadata)
        self.__dd("(AdminAddS2TNode)\n%s" % self.__toJson(resp))
        return self.__toJson(resp)

    def AdminListS2TNodes(self):
        """
        Admin method: implements the gRPC AdminListS2TNodes call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            nodes = []
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.AdminListS2TNodes(empty_pb2.Empty(), metadata=metadata):
                self.__dd("(AdminListS2TNodes)\n%s" % self.__toJson(resp))
                nodes.append(self.__toJson(resp))
        return nodes

    def AdminRemoveS2TNode(self, host, port):
        """
        Admin method: implements the gRPC AdminRemoveS2TNode call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            resp = stub.AdminRemoveS2TNode(mllp_streaming_pb2.RemoveNodeRequest(host=host, port=port), metadata=metadata)
        self.__dd("(AdminRemoveS2TNode)\n%s" % self.__toJson(resp))
        return self.__toJson(resp)


    def AdminAddT2TNode(self, host, port):
        """
        Admin method: implements the gRPC AdminAddT2TNode call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            resp = stub.AdminAddT2TNode(mllp_streaming_pb2.AddNodeRequest(host=host, port=port), metadata=metadata)
        self.__dd("(AdminAddT2TNode)\n%s" % self.__toJson(resp))
        return self.__toJson(resp)

    def AdminListT2TNodes(self):
        """
        Admin method: implements the gRPC AdminListT2TNodes call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            nodes = []
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.AdminListT2TNodes(empty_pb2.Empty(), metadata=metadata):
                self.__dd("(AdminListT2TNodes)\n%s" % self.__toJson(resp))
                nodes.append(self.__toJson(resp))
        return nodes

    def AdminRemoveT2TNode(self, host, port):
        """
        Admin method: implements the gRPC AdminRemoveT2TNode call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            resp = stub.AdminRemoveT2TNode(mllp_streaming_pb2.RemoveNodeRequest(host=host, port=port), metadata=metadata)
        self.__dd("(AdminRemoveT2TNode)\n%s" % self.__toJson(resp))
        return self.__toJson(resp)

    def AdminAddT2SNode(self, host, port):
        """
        Admin method: implements the gRPC AdminAddT2SNode call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            resp = stub.AdminAddT2SNode(mllp_streaming_pb2.AddNodeRequest(host=host, port=port), metadata=metadata)
        self.__dd("(AdminAddT2SNode)\n%s" % self.__toJson(resp))
        return self.__toJson(resp)

    def AdminListT2SNodes(self):
        """
        Admin method: implements the gRPC AdminListT2SNodes call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            nodes = []
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            for resp in stub.AdminListT2SNodes(empty_pb2.Empty(), metadata=metadata):
                self.__dd("(AdminListT2SNodes)\n%s" % self.__toJson(resp))
                nodes.append(self.__toJson(resp))
        return nodes

    def AdminRemoveT2SNode(self, host, port):
        """
        Admin method: implements the gRPC AdminRemoveT2SNode call.
        """

        if not(self.__isAuth()):
           self.AuthToken()
        with self.__createChannel() as channel:
            stub = mllp_streaming_pb2_grpc.MLLPStreamingStub(channel)
            if self._ssl_credentials == None:
                metadata = [(MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._auth_token)] 
            else:
                metadata=None
            resp = stub.AdminRemoveT2SNode(mllp_streaming_pb2.RemoveNodeRequest(host=host, port=port), metadata=metadata)
        self.__dd("(AdminRemoveT2SNode)\n%s" % self.__toJson(resp))
        return self.__toJson(resp)


 
    class _AuthGateway(grpc.AuthMetadataPlugin):
        """
        Internal class to provide authentication token as metadata in all gRPC calls.
        """

        def __init__(self, jwt):
            self._jwt = jwt
    
        def __call__(self, context, callback):
            callback(((MLLPStreamingClient._SIGNATURE_HEADER_KEY, self._jwt),), None)
    
    
