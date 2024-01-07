################################################################################
# Key Tools
#
# This module contains utilities that help with parsing and generating keys
# that are used with Disid. Keys are not required for use but provide an
# increased level of obfuscation to the casual observer. They function as
# substitution ciphers for each letter of the ID which helps disguise simple
# patterns found in the ID. Adding a key does not add any meaningful level of
# security to the IDs against a dedicated attacker however. Disid is not meant
# to be used in and should not be used in any situation where the original
# integer ID must not be shared with the user
################################################################################
from typing import List, Dict
import os

key_chunk_size = 37


################################################################################
# generate_key
#
# Generates a new key to be used with Disid. Returns a bytes object
# containing a valid 190 byte long key which can be used for a 5 character long
# disguised value unless the size parameter is passed in, in which case a
# different length key will be returned instead.
################################################################################
def generate_key(size: int = 5) -> bytes:
    return b''.join([_generate_key_chunk() for _ in range(size)])


################################################################################
# convert_key_to_character_list
#
# Takes in a key, like one generated from generate_key(), and transforms it
# into an array of character lists that can be used to generate the Disid.
################################################################################
def convert_key_to_character_lists(key: bytes) -> List[str]:
    if len(key) % key_chunk_size != 0:
        raise ValueError("Key must be a multiple of key_chunk_size bytes")

    index = 0
    memkey = memoryview(key)

    character_lists = []

    while index + key_chunk_size <= len(memkey):
        character_lists.append(
            _character_list_from_index(int.from_bytes(memkey[index:index + key_chunk_size], 'big'))
        )
        index += key_chunk_size

    return character_lists


################################################################################
# generate_key_chunk
#
# Generates a chunk of the key, representative of a single permutation of one
# of the characters in the id.
################################################################################
def _generate_key_chunk() -> bytes:
    key_chunk = os.urandom(key_chunk_size)

    key_int = int.from_bytes(key_chunk, 'big')

    # A "slow and dumb" way to make sure we have a valid chunk of bytes, but
    # there is only a 0.3% chance of that happening [1-64!/2^(37*8) = 0.00336]
    # so it will basically have no impact on performance making this pretty
    # fast on average.
    while key_int >= _factorial(64):
        key_chunk = os.urandom(key_chunk_size)
        key_int = int.from_bytes(key_chunk, 'big')

    return key_chunk


################################################################################
# character_list_from_index
#
# This function takes in an index of one of the 64! permutations of the 64
# characters, and returns a string with the characters in that particular
# permutation. The characters list is the base64 character set except for the
# two symbols are `-` and `_` instead of `+` and `/`.
################################################################################
characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"


def _character_list_from_index(index: int) -> str:
    permutation: List[int] = _permutation_from_index(64, index)
    return "".join([characters[i] for i in permutation])


################################################################################
# permutation_from_index
#
# Returns an array of length `length` with one of the possible permutations of
# integers from `0` to `length-1`. The index value can be any value between and
# including 0 and factorial(length)-1. This operation is deterministic so the
# same combination of  length and index will always return the same
# permutation. This function does not calculate all the permutations, reducing
# the complexity to  O(LOG(length!)), mostly due to handling large integer
# values of `index`.
################################################################################
def _permutation_from_index(length: int, index: int) -> List[int]:
    # Sanity check that the permutation index is a valid index.
    if index >= _factorial(length) or index < 0:
        raise ValueError("Index out of bounds")

    # Transform the index into an array of possible options with the maximum
    # value of each element being the number of remaining options available for
    # values at that index. The maximum values would be:
    #
    #     [length-1, length-2, length-3, length-4, ... , 3, 2, 1, 0]
    #
    # The last element will always be 0 because the final element only ever has
    # a single option remaining, leaving this 0 in the array makes the next
    # part of this function simpler.
    permutation: List[int] = []
    for i in range(length):
        permutation.append(index // _factorial(length - i - 1))
        index = index % _factorial(length - i - 1)

    # Convert the permutation array of decreasing maximum values into a non
    # repeating array containing all values between and including 0 and
    # length-1 by removing previously chosen values from a list of all possible
    # values before the next element chooses a value.
    options = [option for option in range(length)]
    value: List[int] = []
    for i in permutation:
        value.append(options.pop(i))
    return value


################################################################################
# factorial
#
# A memoized factorial function.
################################################################################
_factorials: Dict[int, int] = {0: 1, 1: 1}


def _factorial(i: int) -> int:
    global _factorials

    if i not in _factorials:
        _factorials[i] = _factorial(i - 1) * i

    return _factorials[i]
