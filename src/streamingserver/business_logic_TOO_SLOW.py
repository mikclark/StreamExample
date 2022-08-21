import logging
import random
import struct
from typing import Generator

OneFile = list[int]
FILE_VALUE_BYTES_SIZE = 2
FILE_VALUE_BYTES_TYPE = 'h'

def create_file_of_random_values(length : int, seed : int = None) -> OneFile:
    logging.info(f"create_file_of_random_values(length={length}, seed={seed}")
    random.seed(seed)
    limitval = pow(2,15)
    file = [random.randrange(-limitval, limitval) for i in range(length)]
    return file


def encode_file_to_bytes(file : OneFile) -> bytes:
    '''Encode a file as bytes in BIG ENDIAN representation. Each value is
    encoded as type = `FILE_VALUE_BYTES_TYPE`.

    If the data provided is incompatible, this function raises an exception.
    
    NOTE: Do NOT replace this with naive `array` or `bytes` operations. This
    server should run consistantly on any operating system for any client,
    and endianness must be 'big' regardless of sys.byteorder.'''
    # ">" means big endian in the `struct` module
    fmt = ">" + FILE_VALUE_BYTES_TYPE * len(file)
    bytes_array = struct.pack(fmt, *file)
    return bytes_array


def generator_random_files(n_files : int,
        file_length_seed : int = None,
        file_seed : int = None
        ) -> Generator[OneFile, None, None]:
    '''
    Generates `n_files` files of random length, each with random values.
    `file_length_seed` is used to seed the random file lengths.
    `file_seed` is used to seed the random values of the files themselves.
    All files use the same file_seed, thus the values of all files will be
    identical if a `file_seed` is given.
    '''
    random.seed(file_length_seed)
    random_file_lengths_kb = [random.randint(1,1024) for i in range(n_files)]

    values_per_kb = int(1024 / FILE_VALUE_BYTES_SIZE)
    for n_kb in random_file_lengths_kb:
        # Create files that are 1KB to 1MB in size
        length = n_kb * values_per_kb
        yield create_file_of_random_values(length, file_seed)
