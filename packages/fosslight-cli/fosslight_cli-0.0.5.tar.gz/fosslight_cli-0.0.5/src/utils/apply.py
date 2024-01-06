from typing import List


def has_key(data: dict, key_list: List[str]):
    result = data
    for key in key_list:
        result = result.get(key)
        if result is None:
            return False
    return True
