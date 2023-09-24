from typing import List, Dict, Union, Any


# Returns True if the argument is a list of lists or dictionaries that have the same number of elements.
def has_homogeneous_shape(l: List[Union[List, Dict]]) -> bool:
    return all(len(item) == len(l[0]) for item in l)


def has_homogeneous_shape_pairs(l: List[tuple]) -> bool:
    return has_homogeneous_shape([list(item[1]) for item in l])


# Returns True if the argument is a list of dictionaries and all dictionaries have the same keys.
def has_homogeneous_keys(l: List[Dict]) -> bool:
    if not isinstance(l[0], dict):
        return False
    first_keys = sorted(l[0].keys())
    return all(sorted(item.keys()) == first_keys for item in l)


# Returns True if the argument is a list of dictionaries and the value types of all dictionaries are the same.
def has_homogeneous_hash_types(l: List[Dict]) -> bool:
    if not isinstance(l[0], dict):
        return False
    first_types = [type(val).__name__ for val in l[0].values()]
    return all([type(val).__name__ for val in item.values()] == first_types for item in l)


# Returns True if the argument is a list of lists and the element types of all lists are the same.
def has_homogeneous_array_types(l: List[List]) -> bool:
    if not isinstance(l[0], (list, tuple)):
        return False
    first_types = [type(val).__name__ for val in l[0]]
    return all([type(val).__name__ for val in item] == first_types for item in l)


def is_array_of_key_array_pairs(arr: List[tuple]) -> bool:
    return all(is_key_array_pair(item) for item in arr) and has_homogeneous_shape_pairs(arr)


def is_key_array_pair(p: tuple) -> bool:
    return isinstance(p[0], str) and isinstance(p[1], (list, tuple))


def is_array_of_key_hash_pairs(arr: List[tuple]) -> bool:
    return all(is_key_hash_pair(item) for item in arr) and has_homogeneous_shape_pairs(arr)


def is_key_hash_pair(p: tuple) -> bool:
    return isinstance(p[0], str) and isinstance(p[1], dict)


def is_array_of_hashes(arr: List) -> bool:
    return all(isinstance(item, dict) for item in arr)


def is_hash_of_hashes(obj: Dict) -> bool:
    return all(isinstance(item, dict) for item in obj.values())


def is_array_of_pairs(obj: List) -> bool:
    return all(isinstance(item, tuple) for item in obj)
