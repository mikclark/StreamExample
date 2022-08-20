from streamingserver.streaming_server import stream
def test_stream_output():
    for i in stream()[0]:
        print(i)
        assert isinstance(i,str)
        n = int(i[0]) if len(i) else 0
        assert len(i) == n*128
