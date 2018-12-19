two_16 = 1 << 16
two_14 = 1 << 14
two_13 = 1 << 13
two_12 = 1 << 12
two_11 = 1 << 11


def binary_string(number):
    ret = "{0:b}".format(number).zfill(16)
    return ret


def rotate_left(number, digit):
    diviser = 1 << (16 - digit)
    quotient = number // diviser
    remainder = number % diviser
    return (remainder << digit) + quotient


def calc_output(input):

    a = input // two_16
    a = rotate_left(a, 6)

    b = input % two_16
    b = rotate_left(b, 9)

    a_tmp = a ^ int('0100101011111110', 2)
    b_tmp = b ^ int('0100000011011110', 2)

    sum = a_tmp + b_tmp
    sum = sum % two_16

    sum_masked = sum ^ int('1101111010101101', 2)

    a = rotate_left(a, 4)
    b = rotate_left(b, 2)

    a_masked = a & int('1010101010101010', 2)
    b_masked = b & int('0101010101010101', 2)
    mask = a_masked + b_masked
    mask = mask ^ int('0111110111110111', 2)

    return sum_masked | mask


def adjust_output(raw_output):
    """ 14 in the output indexes is bit_12 | bit_13, counted from right to left starting from 1"""
    remainder = raw_output % two_11
    quotient = raw_output // two_11
    bit_12 = quotient % 2
    bit_13 = (quotient % 4) // 2
    new_bit_12 = bit_12 | bit_13
    upper_bits = quotient // 4
    return upper_bits * two_12 + new_bit_12 * two_11 + remainder


def get_real_output(output):
    idxes = [123, 119, 96, 14, 173, 160, 163, 167, 154, 158, 145, 148, 136, 140, 128]

    output = list(output)
    output = ''.join([output[idx] for idx in idxes])
    return int(output, 2)


with open("training_data", "r") as data_file:
    for line in data_file:
        line = line.strip()
        input, output = line.split(',')
        calculated_output = adjust_output(calc_output(int(input, 2)))
        real_output = get_real_output(output)
        assert calculated_output == real_output
