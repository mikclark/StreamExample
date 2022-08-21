import pytest
import struct
import time
from typing import Any
from streamingserver.business_logic import generator_random_encoded_files

@pytest.mark.parametrize("n_files", [0,1,10,100])
def test_valid_n_files(n_files):
    files = list(generator_random_encoded_files(n_files))
    assert len(files) == n_files
    assert all(isinstance(f, bytes) for f in files)


@pytest.mark.parametrize("bad_n_files", [ 1.5, [], {}, None ])
def test_bad_n_files(bad_n_files : Any):
    expected_error = "cannot be interpreted as an integer"
    with pytest.raises(Exception) as ex:
        next(generator_random_encoded_files(bad_n_files))
    assert expected_error in str(ex.value)


@pytest.mark.parametrize("seed1, seed2, expected_equal_lengths", [
    [None, None, False],
    [1234, None, False],
    [None, 1234, False],
    [1234, 4321, False],
    [1234, 1234, True],
    [-1, -1,   True],
    [-1, 1234, False],
    [1234, -1, False],
    ])
def test_file_length_seed(seed1:int, seed2:int, expected_equal_lengths:bool):
    n_files = 20
    lengths1 = [len(f) for f in generator_random_encoded_files(n_files, seed1)]
    lengths2 = [len(f) for f in generator_random_encoded_files(n_files, seed2)]
    if expected_equal_lengths:
        assert lengths1 == lengths2
    else:
        assert lengths1 != lengths2


@pytest.mark.parametrize("seed1, seed2, expected_equal_values", [
    [None, None, False],
    [1234, None, False],
    [None, 1234, False],
    [1234, 4321, False],
    [1234, 1234, True],
    [-1, -1,   True],
    [-1, 1234, False],
    [1234, -1, False],
    ])
def test_file_seed(seed1:int, seed2:int, expected_equal_values:bool):
    n_files = 10
    length_seed = 1234
    
    files1 = list(generator_random_encoded_files(n_files, length_seed, seed1))
    files2 = list(generator_random_encoded_files(n_files, length_seed, seed2))
    assert len(files1) == len(files2) == n_files
    for f1, f2 in zip(files1, files2):
        assert len(f1) == len(f2)
        if expected_equal_values:
            assert f1 == f2
        else:
            assert f1 != f2


@pytest.mark.parametrize("bad_seed", [ [], {} ])
def test_invalid_seeds(bad_seed : Any):
    n_files = 10
    good_seed = 1234
    with pytest.raises(TypeError):
        next(generator_random_encoded_files(n_files, good_seed, bad_seed))
    with pytest.raises(TypeError):
        next(generator_random_encoded_files(n_files, bad_seed, good_seed))
