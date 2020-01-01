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


def main(raw_data: str):
    data = json.loads(raw_data)
    yield sum_numbers(data)
    yield sum_numbers(data, exclude={"red"})
