# The MLLP-TTP gRPC Streaming API client Python3 module

The [MLLP-TTP](https://ttp.mllp.upv.es/) gRPC Streaming API client Python3 module implements a client library of the [MLLP-TTP gRPC Streaming
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

## Changelog

- 1.0.0 (2024-01-05):
  + First (independent and corrected) version, matching API version 1.0.

## Installation

Via [Pypi.org](https://pypi.org/project/MLLPStreamingClient/): 

```bash
pip3 install MLLPStreamingClient 
```

Via a provided `.whl` file: 

```bash
pip3 install MLLPStreamingClient-${VERSION}-py3-none-any.whl 
```

Using this repository:

```bash
pip3 install -r requirements.txt
make prep
python3 setup.py install
```
