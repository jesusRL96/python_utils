from collections.abc import MutableMapping

def _flatten_dict_gen(d, parent_key, delimiter):
    for k, v in d.items():
        new_key = parent_key + delimiter + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, delimiter=delimiter).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', delimiter: str = '.'):
    return dict(_flatten_dict_gen(d, parent_key, delimiter))


def insert(dct, lst):
    for x in lst[:-2]:
        dct[x] = dct = dct.get(x, dict())
    dct.update({lst[-2]: lst[-1]})
 
def nest_dict(dct, split='.'):
    # empty dict to store the result
    result = dict()
 
    # create an iterator of lists
    # representing nested or hierarchical flow
    lists = ([*k.split(split), v] for k, v in dct.items())
 
    # insert each list into the result
    for lst in lists:
        insert(result, lst)
    return result