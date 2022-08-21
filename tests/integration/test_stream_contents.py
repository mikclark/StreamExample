import pytest
from streamingserver.streaming_server import stream_too_slow, stream

# WARNING: This test can take up to 5 minutes to run
def test_streamSLOW_contents_default():
    all_files = list(stream_too_slow()[0])
    assert len(all_files) == 100

# WARNING: This test can take up to 2 minutes to run
def test_stream_contents_with_param():
    all_files = list(stream()[0])
    assert len(all_files) == 100

@pytest.mark.parametrize("n_files", [1,4,10])
def test_streamSLOW_contents_with_param(n_files):
    all_files = list(stream_too_slow(n_files)[0])
    assert len(all_files) == n_files

@pytest.mark.parametrize("n_files", [1,4,10])
def test_stream_contents_with_param(n_files):
    all_files = list(stream(n_files)[0])
    assert len(all_files) == n_files

@pytest.mark.parametrize("bad_n_files", [1.5, "a", None])
def test_streamSLOW_with_bad_param(bad_n_files):
    with pytest.raises(Exception):
        next(stream_too_slow(bad_n_files)[0])

@pytest.mark.parametrize("bad_n_files", [1.5, "a", None])
def test_stream_with_bad_param(bad_n_files):
    with pytest.raises(Exception):
        next(stream(bad_n_files)[0])
