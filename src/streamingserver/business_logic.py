import logging
import random
from typing import Generator

def generator_random_encoded_files(n_files : int,
        file_length_seed : int = None,
        file_seed : int = None
        ) -> Generator[bytes, None, None]:
    '''
    Generates `n_files` files of random length, each with random values.
    `file_length_seed` is used to seed the random file lengths.
    `file_seed` is used to seed the random values of the files themselves.
    All files use the same file_seed, thus the values of all files will be
    identical if a `file_seed` is given.
    '''
    random.seed(file_length_seed)
    random_file_lengths_kb = [random.randint(1,1024) for i in range(n_files)]

    for i, n_kb in enumerate(random_file_lengths_kb):
        # Create files that are 1KB to 1MB in size
        length = n_kb * 1024
        logging.info(f"Generating file #{i+1} of {n_files}, length={length}")
        random.seed(file_seed)
        yield random.randbytes(length)
