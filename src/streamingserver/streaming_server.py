import logging
import random
import time
from flask import Flask
from typing import Generator
from streamingserver.business_logic import generator_random_encoded_files
from streamingserver.business_logic_TOO_SLOW import \
        generator_random_files, encode_file_to_bytes, OneFile

app = Flask(__name__)

@app.route('/')
def null_request() -> str:
    logging.info("Request received: null_request")
    return "You have reached streamingserver"



def generator_encoded_files_SLOW(n_files : int) -> Generator[bytes, None, None]:
    '''
    Quoted from the assignment requirements:
    "Generates `n_files` binary files of random sizes ranging from 1KB to 1MB
    at random time intervals randing from 1ms to 1s and encoded as int16."
    '''
    for i, file in enumerate(generator_random_files(n_files)):
        seconds = random.uniform(0.001, 1.0)
        time.sleep(seconds)
        file_as_bytes = encode_file_to_bytes(file)
        logging.info(f"Send file # {i+1}")
        yield file_as_bytes

@app.route('/streamSLOW')
@app.route('/streamSLOW/<int:n_files>')
def stream_too_slow(n_files=100):
    '''
    THIS IS NOT A GOOD FUNCTION TO EMULATE STREAMING.

    This was my first attempt, but the performance wasn't very good: the
    responses arrived with as much as 2 seconds' delay in between, which
    wasn't the requirement. The integer-generation and encoding are too
    slow and represent a bottlneck for the whole request.
    '''
    logging.info("Request received: stream")
    logging.info(f"Returning {n_files} files of random length and contents")
    mimetype = {"Content-type": "application/octet-stream"}
    return generator_encoded_files_SLOW(n_files), mimetype



def generator_encoded_files_FAST(n_files : int) -> Generator[bytes, None, None]:
    '''
    Quoted from the assignment requirements:
    "Generates `n_files` binary files of random sizes ranging from 1KB to 1MB
    at random time intervals randing from 1ms to 1s and encoded as int16."
    '''
    for i, file in enumerate(generator_random_encoded_files(n_files)):
        seconds = random.uniform(0.001, 1.0)
        time.sleep(seconds)
        logging.info(f"Send file # {i+1}")
        yield file

@app.route('/stream')
@app.route('/stream/<int:n_files>')
def stream(n_files=100):
    '''
    THIS IS THE BETTER FUNCTION/REQUEST to emulate streaming.

    This function is much faster because the random files are generated as
    bytes directly, instead of first generating the integers and then encoding
    them. This request is much more representative of what would happen
    if the server process already had access to the 1kb-1MB files, versus the
    streamSLOW request which must take processor time to generate the files.
    '''
    logging.info("Request received: stream")
    logging.info(f"Returning {n_files} files of random length and contents")
    mimetype = {"Content-type": "application/octet-stream"}
    return generator_encoded_files_FAST(n_files), mimetype



def start_server() -> None:
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s"
            )
    app.run(host="127.198.3.14", port=81)


if __name__ == "__main__":
    start_server()
