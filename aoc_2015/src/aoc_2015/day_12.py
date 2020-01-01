import json

def sum_numbers(data, exclude=()):
    if isinstance(data, int):
        return data
    if isinstance(data, list):
        res = 0
        for value in data:
            res += sum_numbers(value, exclude)
        return res
    if isinstance(data, dict):
        res = 0
        for key, value in data.items():
            if isinstance(value, str) and value in exclude:
                return 0
            res += sum_numbers(value, exclude)
        return res
    return 0

def sum_nums_in_json(raw_data: str):
    return sum_numbers(json.loads(raw_data))

def sum_nums_in_json_2(raw_data: str):
    return sum_numbers(json.loads(raw_data), exclude={"red"})

if __name__ == '__main__':
    from libaoc import simple_main, files
    simple_main(2015, 12, files.read_full, sum_nums_in_json, sum_nums_in_json_2)
