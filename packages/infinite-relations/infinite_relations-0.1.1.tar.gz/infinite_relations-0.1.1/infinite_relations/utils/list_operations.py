"""Utility functions for work with lists"""


def compare_lists_orderless(list: list, list_2: list) -> bool:
    """Returns True if both lists containg the same items"""
    return len(list) == len(list_2) and all(item in list_2 for item in list)


def flatten_list(list_of_lists: list) -> list:
    """Creates a list from a list of lists"""
    return [item for sublist in list_of_lists for item in sublist]


def dict_from_lists(keys: list, values: list) -> dict:
    """Creates a dict from a list of keys and list of values"""
    if len(values) != len(keys):
        raise Exception("Number of keys and values doesn't match")

    return dict(zip(keys, values))


def dict_values(dict: dict, keys: list) -> list:
    """Gets a list of values corresponding to a list of keys from a dict

    Parameters
    ----------
    dict : dict
        Dict to get values from
    keys : list
        Subset of keys of the dict

    Returns
    -------
    list
        List of dict's values corresponding to keys
    """
    return [dict[key] for key in keys]


def is_subset(list: list, list_2: list) -> bool:
    """Checks if list is a subset of list_2"""
    return all(item in list_2 for item in list)


def subtract(list: list, list_2: list) -> list:
    """Subtracts list_2 from list"""
    return [item for item in list if not item in list_2]
