"""Contains utility functions."""

from itertools import zip_longest
import os
import random

import torch
import Levenshtein

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def shuffle_together(list1, list2):
    """Shuffles two lists together"""
    zip_list = list(zip(list1, list2))
    random.shuffle(zip_list)
    list1, list2 = zip(*zip_list)
    return list1, list2


def divide_dict(src_dict, num):
    """Divide every value of dict by a number."""
    return {key:(value/num) for key, value in src_dict.items()}


def save_model(epoch_num, state, model_save_dir, filename=None):
    """Save PyTorch model."""
    if filename is None:
        filename = 'epoch-{}'.format(epoch_num)
    torch.save(state, os.path.join(model_save_dir, filename))


def pad_lists(lists, pad_int, pad_len=None, dtype=torch.float, device=device):
    """Pad lists (in a list) to make them of equal size and return a tensor."""

    if pad_len is None:
        pad_len = max([len(lst) for lst in lists])
    new_list = []
    for lst in lists:
        if len(lst) < pad_len:
            new_list.append(lst + [pad_int] * (pad_len - len(lst)))
        else:
            new_list.append(lst[:pad_len])
    return torch.tensor(new_list, dtype=dtype, device=device)


def add_dict(dest, src):
    """Add values of one dictionary to another."""
    for key in src.keys():
        if key in dest.keys():
            dest[key] += src[key]
        else:
            dest[key] = src[key]


def add_string_to_key(src_dict, string):
    """Add string to each key of a dictionary."""
    return {'{} {}'.format(string, key):value for key, value in src_dict.items()}


def merge_lists(lists1, lists2):
    """Add two lists of lists."""
    merged_lists = []
    for list1, list2 in zip(lists1, lists2):
        merged_lists.append(list1 + list2)
    return merged_lists


def mean(List):
    """Calculate mean of a list, return 0 if empty."""
    if len(List) != 0:
        return sum(List)/len(List)
    else:
        return 0.0


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def accuracy(predictions, targets):
    """Return fraction of matches between two lists sequentially."""
    correct_count = 0
    for prediction, target in zip(predictions, targets):
        if prediction == target:
            correct_count += 1
    return correct_count / len(predictions)


def average_distance(predictions, targets):
    """Return average Levenshtein distance between two lists containing strings."""
    total_distance = 0
    for prediction, target in zip(predictions, targets):
        total_distance += Levenshtein.distance(prediction, target)
    return total_distance / len(predictions)
