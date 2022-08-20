from streamingserver.streaming_server import null_request
def test_null_request():
    assert null_request() == "You have reached streamingserver"
