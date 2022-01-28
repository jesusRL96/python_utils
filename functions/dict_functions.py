from collections.abc import MutableMapping
import re

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

def unflatten_dict(flatten_dict):
    reg_p = re.compile(r'\[(\d)\]|$')
    
    for key, value in flatten_dict.keys():
        index = reg_p.findall(key)
        if bool(index):
            pass


def insert(dct, lst):
    reg_ex = re.compile(r'\[(\d)\]')
    list_ = []
    for x in lst[:-2]:
        match_ = reg_ex.findall(x)
        # if match_:
            # x = reg_ex.sub('',x)
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


def unflatten_dictionary(field_dict, split='.'):
    field_dict = dict(field_dict)
    new_field_dict = dict()
    field_keys = list(field_dict)
    field_keys.sort()

    for each_key in field_keys:
        field_value = field_dict[each_key]
        processed_key = str(each_key)
        current_key = None
        current_subkey = None
        for i in range(len(processed_key)):
            if processed_key[i] == "[":
                current_key = processed_key[:i]
                start_subscript_index = i + 1
                end_subscript_index = processed_key.index("]")
                current_subkey = int(processed_key[start_subscript_index : end_subscript_index])

                # reserve the remainder descendant keys to be processed later in a recursive call
                if len(processed_key[end_subscript_index:]) > 1:
                    current_subkey = "{}.{}".format(current_subkey, processed_key[end_subscript_index + 2:])
                break
            # next child key is a dictionary
            elif processed_key[i] == split:
                split_work = processed_key.split(split, 1)
                if len(split_work) > 1:
                    current_key, current_subkey = split_work
                else:
                    current_key = split_work[0]
                break

        if current_subkey is not None:
            if current_key.isdigit():
                current_key = int(current_key)
            if current_key not in new_field_dict:
                new_field_dict[current_key] = dict()
            new_field_dict[current_key][current_subkey] = field_value
        else:
            new_field_dict[each_key] = field_value

    # Recursively unflatten each dictionary on each depth before returning back to the caller.
    all_digits = True
    highest_digit = -1
    for each_key, each_item in new_field_dict.items():
        if isinstance(each_item, dict):
            new_field_dict[each_key] = unflatten_dictionary(each_item)

        # validate the keys can safely converted to a sequential list.
        all_digits &= str(each_key).isdigit()
        if all_digits:
            next_digit = int(each_key)
            if next_digit > highest_digit:
                highest_digit = next_digit

    # If all digits and can be sequential order, convert to list.
    if all_digits and highest_digit == (len(new_field_dict) - 1):
        digit_keys = list(new_field_dict)
        digit_keys.sort()
        new_list = []

        for k in digit_keys:
            i = int(k)
            if len(new_list) <= i:
                # Pre-populate missing list elements if the array index keys are out of order
                # and the current element is ahead of the current length boundary.
                while len(new_list) <= i:
                    new_list.append(None)
            new_list[i] = new_field_dict[k]
        new_field_dict = new_list
    return new_field_dict