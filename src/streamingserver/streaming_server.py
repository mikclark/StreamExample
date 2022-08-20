import logging
import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Request received: index")
    return "This is stupid"

@app.route('/stream')
def stream():
    logging.info("Request received: stream")
    def generate():
        for i in range(10):
            time.sleep(0.5)
            logging.info(f"Send part {i+1}")
            yield str(i)*1024
    return generate(), {"Content-type": "text/plain"}


def start_server():
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s %(levelname)s %(message)s"
            )
    app.run(host="127.198.3.14", port=81)

if __name__ == "__main__":
    start_server()
