################################################################################
# Disid
#
# Disid is a tool for converting an integer into a psuedo random id. Its
# purpose is to disguise a lineraly increasing numerical value so that it
# apears to be a random string of letters and numbers. This is not
# cryptographically secure and with enough known consecutive inputs a dedicated
# attacker can easily rebuild the keys. This should only be used to enhance
# the style of a user facing element that could otherwise contain the raw
# integer value.
#
# Every ID and integer have a 1 to 1 mapping, meaning that every ID represents
# a single integer and ever integer represents a single ID.
################################################################################
from typing import List


################################################################################
# uint_to_id_v3
#
# Converts a positive integer into a V3 id string.
################################################################################
def uint_to_id_v3(integer: int, digit_order: List[str]) -> str:
    length = len(digit_order)

    base_64 = uint_to_base64(integer)
    base_64 = pad_zeros(base_64, length)

    for late_index in reversed(range(1, length)):
        for early_index in range(0, late_index):
            base_64[late_index] = base_64[late_index] + (base_64[early_index] + 1) * (late_index - early_index)
        base_64[late_index] = base_64[late_index] % 64

    identifier = ""
    for i in range(length):
        identifier += digit_order[i][base_64[i]]

    return identifier


################################################################################
# id_v2_to_uint
#
# Depricated. Use uint_to_id_v3() and id_v3_to_uint() instead.
# Converts a v2 id value into a positive integer.
################################################################################
def id_v3_to_uint(identifier: str, digit_order: List[str]) -> int:
    length = len(identifier)

    base_64 = []
    for i in range(length):
        base_64.append(digit_order[i].index(identifier[i]))

    for early_index in range(0, length):
        base_64[early_index] = base_64[early_index] % 64
        for late_index in range(early_index + 1, length):
            base_64[late_index] = base_64[late_index] - (base_64[early_index] + 1) * (late_index - early_index)

    # Decode the values into an int
    modifier = 1
    integer = 0
    for digit in base_64:
        integer += digit * modifier
        modifier *= 64

    return integer


################################################################################
# uint_to_id_v2
#
# Depricated. Use unit_to_id_v3() instead. V2 suffers from an issue where
# characters are more likely to show up in a pattern the farther into the id
# you get.
# Converts a positive integer into a V2 id string.
################################################################################
def uint_to_id_v2(integer: int, digit_order: List[str]) -> str:
    base_64 = uint_to_base64(integer)
    base_64 = pad_zeros(base_64, len(digit_order))

    offset = base_64[0] + 1
    for i in range(1, len(digit_order)):
        base_64[i] = (base_64[i] + offset) % 64
        offset += base_64[i]

    identifier = ""
    for i in range(len(digit_order)):
        identifier += digit_order[i][base_64[i]]

    return identifier


################################################################################
# id_v2_to_uint
#
# Depricated. Use uint_to_id_v3() and id_v3_to_uint() instead.
# Converts a v2 id value into a positive integer.
################################################################################
def id_v2_to_uint(identifier: str, digit_order: List[str]) -> int:
    offset_base_64 = []
    for i in range(5):
        offset_base_64.append(digit_order[i].index(identifier[i]))

    base_64 = [offset_base_64[0]]
    offset = offset_base_64[0] + 1
    for i in offset_base_64[1:]:
        base_64.append((i - offset) % 64)
        offset += i

    modifier = 1

    integer = 0

    for digit in base_64:
        integer += digit * modifier
        modifier *= 64

    return integer


################################################################################
# uint_to_id_v1
#
# Depricated. Use unit_to_id_v3() instead. V1 suffers from an issue wher all
# but the first character get repeated nearly every 63 characters.
# Converts a positive integer into a V1 id string.
################################################################################
def uint_to_id_v1(integer: int, digit_order: List[str]) -> str:
    base_64 = uint_to_base64(integer)
    base_64 = pad_zeros(base_64, len(digit_order))

    for i in range(1, len(digit_order)):
        base_64[i] = (base_64[i] + base_64[i - 1]) % 64

    identifier = ""
    for i in range(len(digit_order)):
        identifier += digit_order[i][base_64[i]]

    return identifier


################################################################################
# id_v1_to_uint
#
# Depricated. Use uint_to_id_v3() and id_v3_to_uint() instead.
# Converts a v1 id value into a positive integer.
################################################################################
def id_v1_to_uint(identifier: str, digit_order: List[str]) -> int:
    base_64 = []
    for i in range(5):
        base_64.append(digit_order[i].index(identifier[i]))

    for i in range(4, 0, -1):
        base_64[i] = (base_64[i] - base_64[i - 1]) % 64

    modifier = 1

    integer = 0

    for digit in base_64:
        integer += digit * modifier
        modifier *= 64

    return integer


################################################################################
# int_to_base64
#
# Converts a regular unsigned integer to a list of base64 digits. The first
# element in the returned list is the least significant digit. If a negative
# number is received it will error.
#
# TODO: Because this is just base64 now instead of any base we can take
# advantage of bit-slicing and bitwise operators to make this faster.
################################################################################
def uint_to_base64(x: int) -> List[int]:
    if x < 0:
        raise ValueError("Cannot turn negative int into base64.")
    elif x == 0:
        return [0]

    digits = []

    while x:
        digits.append(int(x % 64))
        x = int(x / 64)

    return digits


################################################################################
# pad_zeros
#
# A helper function to add 0's to the end of the digit list to make it five
# elements long.
################################################################################
def pad_zeros(array: List[int], length: int = 5) -> List[int]:
    delta_length = length - len(array)

    for _ in range(delta_length):
        array.append(0)

    return array
