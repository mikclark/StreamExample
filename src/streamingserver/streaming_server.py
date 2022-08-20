import logging
import random
import time
from flask import Flask
from streamingserver.business_logic import \
        generator_random_files, encode_file_to_bytes

app = Flask(__name__)

def generator_encoded_files(n_files):
    ''''''
    for file in generator_random_files(n_files):
        seconds = random.uniform(0.001, 1.0)
        time.sleep(seconds)
        file_as_bytes = encode_file_to_bytes(file)
        logging.info(f"Send file # {i+1}")
        yield file_as_bytes


@app.route('/')
def null_request():
    logging.info("Request received: null_request")
    return "You have reached streamingserver"


@app.route('/stream')
@app.route('/stream/<int:n_files>')
def stream(n_files=100):
    logging.info("Request received: stream")
    logging.info(f"Returning {n_files} files of random length and contents")
    mimetype = {"Content-type": "application/octet-stream"}
    return generator_encoded_files(100), mimetype


def start_server():
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s"
            )
    app.run(host="127.198.3.14", port=81)


if __name__ == "__main__":
    start_server()
