import pytest
import numpy as np
from npstructures import HashTable, Counter, HashSet


@pytest.fixture
def array_list():
    return [[0, 1, 2], [2, 1], [1, 2, 3, 4], [3]]


@pytest.mark.parametrize("cls", [HashTable])
def test_lookup(cls):
    keys = [0, 3, 7, 11, 13, 17, 19, 23, 29, 31]
    values = np.arange(len(keys))
    table = cls(keys, values, 7)
    assert np.all(table[keys] == values)
    assert np.all(table[keys][::-1] == values[::-1])


@pytest.mark.parametrize("cls", [HashTable])
def test_lookup_int(cls):
    keys = [0, 3, 7, 11, 13, 17, 19, 23, 29, 31]
    values = np.arange(len(keys))
    table = cls(keys, values, 7)
    assert table[11] == 3


@pytest.mark.parametrize("cls", [HashTable])  # , IHashTable])
def test_lookup_small(cls):
    keys = [0, 3]
    values = np.arange(len(keys))
    table = cls(keys, values, 17)
    assert np.all(table[keys] == values)
    assert np.all(table[keys][::-1] == values[::-1])


@pytest.mark.parametrize("cls", [HashTable])
def test_setitem_int(cls):
    keys = [0, 3, 7, 11, 13, 17, 19, 23, 29, 31]
    values = np.arange(len(keys))
    table = cls(keys, values, 7)
    table[11] = 10
    values[3] = 10
    assert table == cls(keys, values, 7)


@pytest.mark.parametrize("cls", [HashTable])
def test_setitem_list(cls):
    keys = [0, 3, 7, 11, 13, 17, 19, 23, 29, 31]
    values = np.arange(len(keys))
    table = cls(keys, values, 7)
    table[[11, 19, 29]] = [10, 11, 12]
    values[[3, 6, 8]] = [10, 11, 12]
    assert table == cls(keys, values, 7)


def test_count():
    keys = [0, 3, 7, 11, 13, 17, 19, 23, 29, 31]
    counter = Counter(keys, mod=17)
    samples = [9, 0, 3, 12, 3, 7, 10, 7, 7, 2, 3, 0]
    counter.count(samples)
    assert np.all(counter[[0, 3, 7]] == [2, 3, 3])
    assert np.all(counter[[11, 13, 17, 19, 23, 29, 31]] == 0)


def test_count_bug():
    keys = [1, 2, 3, 4]
    counter = Counter(keys)
    samples = [3, 4]
    counter.count(samples)
    assert np.all(counter[[3, 4]] == [1, 1])
    assert np.all(counter[[1, 2]] == [0, 0])


def test_count_empty():
    keys = [1, 2, 3, 4]
    counter = Counter(keys)
    samples = [0, 0]
    counter.count(samples)
    assert np.all(counter[[1, 2, 3, 4]] == 0)


def test_count_large():
    keys = [2 ** 55 - 1, 2 ** 62 - 1]
    counter = Counter(keys, key_dtype=np.int64)
    samples = [0, 2 ** 62 - 1]
    counter.count(samples)
    assert np.all(counter[[2 ** 55 - 1, 2 ** 62 - 1]] == [0, 1])


def test_count_many_large():
    keys = 2 ** 62 - np.arange(20)
    counter = Counter(keys, key_dtype=np.int64)
    samples = np.concatenate([keys, keys])
    counter.count(samples)
    assert np.all(counter[keys] == 2)


def test_iterative_counts():
    keys = [1, 2, 3, 4]
    counter = Counter(keys)
    counter.count([3, 4])
    assert np.all(counter[[1, 2, 3, 4]] == [0, 0, 1, 1])

    counter.count([1, 2])
    assert np.all(counter[[1, 2, 3, 4]] == [1, 1, 1, 1])

    counter.count([])
    assert np.all(counter[[1, 2, 3, 4]] == [1, 1, 1, 1])

    counter.count([0, 5, 6, 7])
    assert np.all(counter[[1, 2, 3, 4]] == [1, 1, 1, 1])

    counter.count([7, 6, 5, 4])
    assert np.all(counter[[1, 2, 3, 4]] == [1, 1, 1, 2])


def test_hashset():
    keys = HashSet([0, 1, 3, 17])
    lookup = [0, 0, 3, 2, 1, 5]
    in_keys = keys.contains(lookup)
    print(in_keys)
    assert np.all(in_keys == [True, True, True, False, True, False])
