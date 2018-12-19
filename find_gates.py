import numpy as np
import itertools


def is_const0(vec):
    return np.sum(vec) == 0


def is_const1(vec):
    return np.sum(vec) == vec.shape[0] * 255


def is_equal(vec1, vec2):
    return np.array_equal(vec1, vec2)


def is_not(vec1, vec2):
    return np.array_equal(np.bitwise_not(vec1), vec2)


def is_and(vec_o, vec_i1, vec_i2):
    vec_and = np.bitwise_and(vec_i1, vec_i2)
    return np.array_equal(vec_o, vec_and)


def is_or(vec_o, vec_i1, vec_i2):
    vec_or = np.bitwise_or(vec_i1, vec_i2)
    return np.array_equal(vec_o, vec_or)


def is_xor(vec_o, vec_i1, vec_i2):
    vec_xor = np.bitwise_xor(vec_i1, vec_i2)
    return np.array_equal(vec_o, vec_xor)


def is_and3(vec_o, vec_i1, vec_i2, vec_i3):
    vec_and2 = np.bitwise_and(vec_i1, vec_i2)
    vec_and3 = np.bitwise_and(vec_and2, vec_i3)
    return np.array_equal(vec_o, vec_and3)


def is_or3(vec_o, vec_i1, vec_i2, vec_i3):
    vec_or2 = np.bitwise_or(vec_i1, vec_i2)
    vec_or3 = np.bitwise_or(vec_or2, vec_i3)
    return np.array_equal(vec_o, vec_or3)


def is_xor3(vec_o, vec_i1, vec_i2, vec_i3):
    vec_xor2 = np.bitwise_xor(vec_i1, vec_i2)
    vec_xor3 = np.bitwise_xor(vec_xor2, vec_i3)
    return np.array_equal(vec_o, vec_xor3)


# Read data
def read_data():
    with open("training_data", "r") as data_file:
        i = []
        o = []
        for line in data_file:
            this_i, this_o = line.strip().split(',')
            this_i = list(map(int, this_i))
            this_o = list(map(int, this_o))
            i.append(this_i)
            o.append(this_o)
        i_mat = np.asarray(i, dtype=np.int)
        rows = i_mat.shape[0]

        # np.packbits packs every 8 bits into an uint_8. It appends 0s at the end and is not desired to learn the gates.
        # For this reason, the last few rows need to be excluded from the iing data.
        rows_exclude = rows % 8
        i_mat = np.packbits(i_mat[0:rows-rows_exclude, :], axis=0)

        o_mat = np.asarray(o, dtype=np.int)
        o_mat = np.packbits(o_mat[0:rows - rows_exclude, :], axis=0)

    return i_mat, o_mat


def find_const(o_mat):
    ret = set()
    for idx in range(o_mat.shape[1]):
        if is_const0(o_mat[:, idx]):
            print(idx, '=', "CONST0")
            ret.add(idx)
        elif is_const1(o_mat[:, idx]):
            print(idx, '=', "CONST1")
            ret.add(idx)
    return ret


def find_not_unique(o_mat):
    ret = set()
    for idx_1, idx_2 in itertools.combinations(range(o_mat.shape[1]), 2):
        if is_equal(o_mat[:, idx_2], o_mat[:, idx_1]):
            ret.add(idx_2)
            print(idx_2, '=', "O", idx_1)
    return ret


def find_input_gates(idx_not_const, o_mat, i_mat):
    ret = set()
    for idx in idx_not_const:
        for i in range(i_mat.shape[1]):
            if is_equal(o_mat[:, idx], i_mat[:, i]):
                print(idx, '=', 'I', i)
                ret.add(idx)
            elif is_not(o_mat[:, idx], i_mat[:, i]):
                print(idx, '=', "NOT_I", i)
                ret.add(idx)
    return ret


def find_unary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat):
    ret = set()
    for idx_1, idx_2 in itertools.product(idx_remaining, idx_last_identified):
        if is_not(o_mat[:, idx_1], o_mat[:, idx_2]):
            ret.add(idx_1)
            print(idx_1, '=', "NOT_O", idx_2)
    return ret


def find_binary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat):
    ret = set()
    idx_all_identified = idx_last_identified.union(idx_old_identified)
    combinations = set(itertools.combinations(idx_all_identified, 2))
    combinations = combinations.difference(itertools.combinations(idx_old_identified, 2))
    for idx_o in idx_remaining:
        for idx_i1, idx_i2 in combinations:
            if is_and(o_mat[:, idx_o], o_mat[:, idx_i1], o_mat[:, idx_i2]):
                ret.add(idx_o)
                print(idx_o, '=', 'AND', idx_i1, idx_i2)
            elif is_or(o_mat[:, idx_o], o_mat[:, idx_i1], o_mat[:, idx_i2]):
                ret.add(idx_o)
                print(idx_o, '=', "OR", idx_i1, idx_i2)
            elif is_xor(o_mat[:, idx_o], o_mat[:, idx_i1], o_mat[:, idx_i2]):
                ret.add(idx_o)
                print(idx_o, '=', "XOR", idx_i1, idx_i2)
    return ret


def find_ternary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat):

    ret = set()
    idx_all_identified = idx_last_identified.union(idx_old_identified)
    combinations = set(itertools.combinations(idx_all_identified, 3))
    combinations = combinations.difference(itertools.combinations(idx_old_identified, 3))
    for idx_o in idx_remaining:
        for idx_i1, idx_i2, idx_i3 in combinations:
            if is_and3(o_mat[:, idx_o], o_mat[:, idx_i1], o_mat[:, idx_i2], o_mat[:, idx_i3]):
                ret.add(idx_o)
                print(idx_o, '=', 'AND3', idx_i1, idx_i2, idx_i3)
            elif is_or3(o_mat[:, idx_o], o_mat[:, idx_i1], o_mat[:, idx_i2], o_mat[:, idx_i3]):
                ret.add(idx_o)
                print(idx_o, '=', "OR3", idx_i1, idx_i2, idx_i3)
            elif is_xor3(o_mat[:, idx_o], o_mat[:, idx_i1], o_mat[:, idx_i2], o_mat[:, idx_i3]):
                ret.add(idx_o)
                print(idx_o, '=', "XOR3", idx_i1, idx_i2, idx_i3)
    return ret


i_mat, o_mat = read_data()
idx_all = set(range(o_mat.shape[1]))
idx_const = find_const(o_mat)
idx_not_unique = find_not_unique(o_mat)
idx_unique_not_const = idx_all.difference(idx_const).difference(idx_not_unique)
idx_input = find_input_gates(idx_unique_not_const, o_mat, i_mat)

idx_last_identified = idx_input  # Assuming const can not be input to gates
idx_remaining = idx_unique_not_const.difference(idx_last_identified)
idx_old_identified = set()

while len(idx_last_identified) != 0:
    idx_unary = find_unary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat)
    idx_binary = find_binary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat)

    idx_old_identified = idx_old_identified.union(idx_last_identified)
    idx_last_identified = idx_unary.union(idx_binary)
    idx_remaining = idx_remaining.difference(idx_last_identified)

# At this point, only [0, 1, 14, 15] cannot be found
# print("Unable to identify:", ' '.join([str(idx) for idx in idx_remaining]))


idx_remain = {0, 1, 14, 15}
find_ternary_gates(idx_remain, idx_unique_not_const.difference(idx_remain), set(), o_mat)

idx_remaining = {0, 1, 15}
idx_last_identified = {14}
idx_old_identified = idx_unique_not_const.difference(idx_remaining).difference(idx_last_identified)
find_ternary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat)

idx_remaining = {0, 1}
idx_last_identified = {15}
idx_old_identified = idx_unique_not_const.difference(idx_remaining).difference(idx_last_identified)
find_ternary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat)

idx_remaining = {1}
idx_last_identified = {0}
idx_old_identified = idx_unique_not_const.difference(idx_remaining).difference(idx_last_identified)
find_ternary_gates(idx_remaining, idx_last_identified, idx_old_identified, o_mat)
