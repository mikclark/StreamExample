# StreamExample

This repo contains code for an elementary server "streamingserver". The streamingserver contains requests at three endpoints:
- "http://127.198.3.14:81/"  -  Simply returns a message. This is to check connectivity.
- "http://127.198.3.14:81/stream" and "http://127.198.3.14:81/streamSLOW"  -  These requests are meant to stream data to the client. As named, the `streamSLOW` endpoint will return data slower.

The purpose of `stream` and `streamSLOW` is to fulfill this requirement: "a local Python server that takes in a simple client request and in response generate 100 binary files of random sizes ranging from 1KB to 1MB at random time intervals ranging from 1ms to 1s and encoded as int16."

## Running and Calling

### Server as pip package

This server is packaged using setuptools and buildable via pip. To install it, run the following command:

`$ pip install git+https://github.com/mikclark/StreamExample.git`

and then run one of the following valid commands. This was tested in both Linux and Windows.
- `$ streamingserver` (on Linux command line or Windows cmd)
- `python[X.Y] -m streamingserver.streaming_server`

The server will then be available on the local machine to be called.

### Calling from a client

Any HTTP client will be able to contact the endpoints listed above. As a preliminary test, simply enter the address "http://127.198.3.14:81/" in your browser, and check if you receive output text from streamingserver.

This repository also contains an [example Python script](client_code_example/client_streamingserver.py) to call the server. The Python script uses the `requests` module and calls both the connectivity endpoint and the "/stream" endpoint. The Python script can be used as a starting point for coding a client for a streaming server such as this one.

### Local testing with pytest
`
There are multiple tests meant to be run via the `pytest` module. They are divided into unit tests and integration tests. As per Python standard practices, the tests will only work if the `streamingserver` package is installed. This is best done with a [Python virtual environment](https://docs.python.org/3/glossary.html#term-virtual-environment) and an [editable install]():

1. create virtual environment
`$ python[X.Y] -m venv local\_venv`

2. activate virtual environment
`$ . local\_venv/bin/activate`

3. install the streamingserver package as an editable install
`$ python -m pip install -e .`

This enables you to run the streamingserver source code via `python -m streamingserver.streaming\_server`, even after you've made edits to the local source code. However, streamingserver is installed as a package, and you can also do things like `import streamingserver` within a Python file.

To run the tests themselves:

4. install the pytest module
`$ python -m pip install pytest`

5. run all the tests
`$ python -m pytest tests`

6. or just run the unit tests, for example
`$ python -m pytest tests/unit`

All other command-line arguments for `pytest` can be found in the [pytest documentation](https://docs.pytest.org).

WARNING: [Two particular integration tests](tests/integration/test_stream_contents.py#L4-L12) invoke the endpoints directly, which means they will wait for the server to response with all data before proceeding. They require several minutes (100 files with an average of 0.5-1.0 seconds of delay between each file) to complete. All other tests run in milliseconds.
