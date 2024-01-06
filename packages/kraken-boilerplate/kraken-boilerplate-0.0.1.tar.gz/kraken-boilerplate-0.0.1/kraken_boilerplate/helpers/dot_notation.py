

"""
Function to transform dict into dot notation capable

Reference: https://stackoverflow.com/questions/66208077/how-to-convert-a-nested-python-dictionary-into-a-simple-namespace

"""

from types import SimpleNamespace

def parse(data):
    if type(data) is list:
        return list(map(parse, data))
    elif type(data) is dict:
        sns = SimpleNamespace()
        for key, value in data.items():
            setattr(sns, key, parse(value))
        return sns
    else:
        return data



def from_dot(record):
    if isinstance(record, list):
        return [from_dot(x) for x in record]

    elif isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            keys = k.split('.')
            current_dict = new_record

            for key in keys[:-1]:
                current_dict = current_dict.setdefault(key, {})

            current_dict[keys[-1]] = v

        return new_record
    else:
        return record


def to_dot(record, keys=[]):
    """
    """

    if isinstance(record, list):
        results = []
        for i in record:
            results += to_dot(i, keys)
        return results

    elif isinstance(record, dict):
        results = []
        for k, v in record.items():
            new_keys = keys + [k]
            results+=to_dot(v,new_keys)
        return results
        
    else:
        result = [{
            'key': '.'.join(keys),
            'value': record
        }]
        return result

        