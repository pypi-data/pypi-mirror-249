import re
from typing import Union


def camel_to_snake(name: str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def snake_to_camel(name: str):
    words = name.split('_')
    result = words[0] + ''.join(word.title() for word in words[1:])
    return result


def convert_dict_to_python_naming(data: Union[dict, list, str, int, float, bool], exclude_shallow: list[str] = [], shallow=False):
    if type(data) == dict:
        result = {}
        for k in data:
            key = camel_to_snake(k)
            convert = not shallow and k not in exclude_shallow and key not in exclude_shallow
            result[key] = convert_dict_to_python_naming(data[k]) if convert else data[k]
    elif type(data) == list:
        result = []
        for x in data:
            result[x] = convert_dict_to_python_naming(data[x], shallow=shallow)
    else:
        result = data

    return result


def dict_to_camel_shallow(data):
    result = {}
    for k in data:
        key = snake_to_camel(k)
        result[key] = data[k]
