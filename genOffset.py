import json
import math
import os

_params = {}


def get_by_tr(tr):
    data = _params.get(tr)
    if not data:
        data = []
        _params[tr] = data
    return data


def extrace_offset(jsonFile, benchmark=36.6):
    records = json.load(open(jsonFile, 'r'))

    trSum = 0.0
    for r in records:
        trSum += r['tr']
    tr = round(trSum / len(records))

    offsetArray = get_by_tr(tr)

    for r in records:
        offset = {
            'originalValue': r['originalValue'],
            'distance': round(r['distance']),
            'offset': benchmark - r['originalValue']
        }
        offsetArray.append(offset)

    # offsetArray = sorted(offsetArray, key=lambda x: x['distance'])

    # data = {
    #     'benchmark': benchmark,
    #     'tr': tr,
    #     'offsets': offsetArray
    # }


def read_training_data():
    file_list = os.listdir("TrainingData")
    for f in file_list:
        benchmark = int(f[-8:-5]) / 10.0
        extrace_offset("TrainingData/" + f, benchmark)


def get_list_from_dict(dict, key):
    data = dict.get(key)
    if not data:
        data = []
        dict[key] = data
    return data


def marge(offsetArray):
    groups = {}
    for offset in offsetArray:
        group = get_list_from_dict(groups, offset['distance'])
        group.append(offset)

    distance_list = groups.keys()
    distance_list = sorted(distance_list)

    values = {}
    for distance in distance_list:
        group = groups[distance]
        sum = 0.0
        for o in group:
            sum += o['offset']
        values[distance] = sum / len(group)

    return values


if __name__ == '__main__':
    read_training_data()
    print(_params.keys())
    final_array = {}
    for k, v in _params.items():
        values = marge(v)
        final_array[k] = values

    json.dump(final_array, open('params.json', 'w'))
    print(len(final_array))
