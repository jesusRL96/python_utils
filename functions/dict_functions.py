import re
import itertools
import operator
from collections.abc import MutableMapping
from functools import reduce

def _flatten_dict_gen(d, parent_key, delimiter):
    if isinstance(d, MutableMapping):
        for k, v in d.items():
            new_key = parent_key + delimiter + k if parent_key else k
            if isinstance(v, MutableMapping):
                yield from flatten_dict(v, new_key, delimiter=delimiter).items()
            elif isinstance(v, list):
                for i,x in enumerate(v):
                    if isinstance(x, MutableMapping):
                        yield from flatten_dict(x, f'{new_key}[{i}]', delimiter=delimiter).items()
                    else:
                        yield from flatten_dict(x, f'{new_key}[{i}]', delimiter=delimiter).items()
            else:
                yield new_key, v
    else:
        yield parent_key, d

def flatten_dict(d: MutableMapping, parent_key: str = '', delimiter: str = '.'):
    return dict(_flatten_dict_gen(d, parent_key, delimiter))


def nest_dict_function(flatten_dict, split='.', left_key='[', right_key=']'):
    n_d = {}
    for index_f, value in flatten_dict.items():
        # keys_list = index_f.split(split)
        keys_list = split_flatten_key(index_f, split, left_key, right_key)
        n_d, _ = reduce(function_reduce, keys_list, (n_d,[]))
        
        reduce(operator.getitem, keys_list[:-1], n_d)[keys_list[-1]] = value
    return n_d

def function_reduce(tup,key):
    d, keys = tup
    try:
        search_keys = [*keys, key]
        reduce(operator.getitem, search_keys, d)
    except KeyError:
        if isinstance(key, int):
            if isinstance(reduce(operator.getitem, keys[:-1], d), list):
                reduce(operator.getitem, keys[:-1], d).append({})
            else:
                reduce(operator.getitem, keys[:-1], d)[keys[-1]] = [{}]

        else:
            reduce(operator.getitem, keys, d)[key] = {}
    except IndexError:
        reduce(operator.getitem, keys, d).append({})
    keys = [*keys, key]
    return d, keys

def split_flatten_key(f_key, split, left_key, right_key):
    split_key = re.split(rf'{re.escape(left_key)}(\d+){re.escape(right_key)}', f_key)
    split_key = [int(x) if x.isnumeric() else x for x in split_key ]
    split_key = array_x if bool(array_x := [x.split(split) if isinstance(x, str) else [x] for x in split_key if x!='']) else []
    return [x for x in list(itertools.chain.from_iterable(split_key)) if x != '']


