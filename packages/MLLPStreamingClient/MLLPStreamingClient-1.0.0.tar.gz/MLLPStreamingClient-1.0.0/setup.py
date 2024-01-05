import setuptools
import glob

def readme():
    with open('doc/md/README.md') as f:
        return f.read()

def version(micro=None):
    with open("VERSION") as f:
        v = f.read().strip()
    if micro == None:
        return v
    else:
        nv = v.split(".")
        nv[-1] = "%s" % micro
        return ".".join(nv)

setuptools.setup(
    name="MLLPStreamingClient",
    version=version(),
    author="MLLP-VRAIN",
    author_email="mllp-support@upv.es",
    description="The MLLP-TTP gRPC Streaming API Python3 client library",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://www.mllp.upv.es",
    project_urls={
        "RPC API documentation": "https://ttp.mllp.upv.es/mllp-streaming-api/1.0/index.html",
        "Python3 client documentation": "https://ttp.mllp.upv.es/mllp-streaming-api/1.0/python3-client-doc.html"
    },
    packages=["MLLPStreamingClient"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.5',
    install_requires=['protobuf==4.22.0',
                      'grpcio==1.51.3', 
                      'grpcio-tools==1.51.3',
                      'pyaudio',
                      'soundfile',
                      'sounddevice'],
    scripts=glob.glob("scripts/mllp-*.py"),
)
