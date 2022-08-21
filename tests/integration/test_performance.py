import time
from streamingserver.streaming_server import stream_too_slow, stream

def test_streamSLOW_performance():
    t0 = None
    print("Calling streamSLOW")
    generator = stream_too_slow(10)[0]
    for i, f in enumerate(generator):
        print(f"Received file {i+1} from /streamSLOW")
        t1 = time.time()
        if t0:
            # The first file has to wait for start-up costs.
            dt = t1 - t0
            assert dt < 3.0
        t0 = t1

def test_stream_performance():
    t0 = None
    print("Calling stream")
    generator = stream(10)[0]
    for i, f in enumerate(generator):
        print(f"Received file {i+1} from /stream")
        t1 = time.time()
        if t0:
            # The first file has to wait for start-up costs.
            dt = t1 - t0
            assert dt < 1.4
        t0 = t1
