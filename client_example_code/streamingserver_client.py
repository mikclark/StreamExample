from datetime import datetime
import requests
import struct

ADDRESS = "http://127.198.3.14:81/"

def _decode(file : bytes):
    n = len(file) >> 1   # Divide in half via bit-shift
    fmt = '>' + 'h'*n    # '>' means big-endian. Decode n integers.
    return struct.unpack(fmt, file)

def _log_the_file(i : int, file : bytes):
    t = datetime.now()
    length_kb = len(file) >> 10
    f = _decode(file)
    print(f"Received file #{i+1} at {t}: ({length_kb} kB) {f[0:8]}...")


def is_server_up():
    response = requests.get(ADDRESS)
    print(response.text)


def get_all_files():
    response = requests.get(f"{ADDRESS}stream", stream=True)
    for i, each_file in enumerate(response.iter_content(None)):
        _log_the_file(i, each_file)


if __name__ == "__main__":
    is_server_up()
    get_all_files()
