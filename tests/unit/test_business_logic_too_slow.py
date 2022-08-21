import pytest
import struct
import time
from typing import Any
from streamingserver.business_logic_TOO_SLOW import \
        create_file_of_random_values, encode_file_to_bytes, \
        generator_random_files, OneFile, FILE_VALUE_BYTES_SIZE


def valid_files() -> list[OneFile]:
    return [
            [1],
            [1,2,3,4,5],
            [-1,0,1],
            list(range(1024)),
            list(range(-1024,0)),
            list(range(0,32768,1024)),
            list(range(-32768,32768,1024))
            ]


def bad_files() -> list[Any]:
    bad_files = []
    for bad_val : Any in [None, 0.5, [], {}]:
        bad_files.extend([
                [bad_val],
                [bad_val, 1, 2, 3],
                [1, 2, 3, bad_val]
                ])
    return bad_files


@pytest.mark.parametrize("length", [1,10,100,1000,10000])
@pytest.mark.parametrize("seed", [None, 1, 123456789])
def test_file_creation_length_and_values(length, seed):
    file = create_file_of_random_values(length, seed)
    assert len(file) == length

    # This part of the test assumes OneFile is a list[int16]
    assert all(isinstance(i,int) for i in file)
    assert all( [(i>=-32768) and (i < 32768) for i in file] )


@pytest.mark.parametrize( "expected_equal,seed1,seed2", [
    (True, 1, 1),
    (True, 123456789, 123456789),
    (False, None, None),
    (False, 1, None),
    (False, None, 1),
    (False, 1, 2),
    (False, 1234, 5678),
    ])
def test_file_creation_seed(expected_equal, seed1, seed2):
    length = 50
    file1 = create_file_of_random_values(length, seed1)
    file2 = create_file_of_random_values(length, seed2)
    if expected_equal:
        assert file1 == file2
    else:
        assert file1 != file2

@pytest.mark.parametrize("file", valid_files())
def test_encode_file_structure(file : OneFile):
    encoded = encode_file_to_bytes(file)
    assert isinstance(encoded, bytes)
    assert len(file) * FILE_VALUE_BYTES_SIZE == len(encoded)


@pytest.mark.parametrize("file", valid_files())
def test_encode_file_big_endian_accuracy(file : OneFile):
    encoded = encode_file_to_bytes(file)
    assert isinstance(encoded, bytes)
    decoded = struct.iter_unpack('>h', encoded)
    for decoded_tuple, original_val in zip(decoded, file):
        assert decoded_tuple[0] == original_val
    # Make doubly sure it is a big-endian
    first_val = encoded[0:FILE_VALUE_BYTES_SIZE]
    decoded_first_val = int.from_bytes(first_val, 'big', signed=True)
    assert decoded_first_val == file[0]

@pytest.mark.parametrize('bad_file',[
    [32768],
    [123456789],
    [1,2,3,4,32768],
    [32768,1,2,3,4],
    list(range(32769)),
    list(range(0,1000000000,1000000))
    ])
def test_encode_file_overflow_failure(bad_file : OneFile):
    with pytest.raises(struct.error) as ex:
        encode_file_to_bytes(bad_file)
        assert "format requires" in repr(ex)

@pytest.mark.parametrize('bad_file', bad_files())
def test_encode_file_nonint_failure(bad_file : OneFile):
    with pytest.raises(struct.error) as ex:
        encode_file_to_bytes(bad_file)
        assert "required argument is not" in repr(ex)
