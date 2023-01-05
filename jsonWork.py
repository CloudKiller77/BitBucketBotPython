import json


def write_last_count(last_count: str, count: int):
    with open("database.json", "w") as fh:
        str_1 = {last_count: count}
        json.dump(str_1, fh, sort_keys=True, indent=2)


def read_last_count() -> json:
    with open("database.json", "r") as fh:
        str_1 = json.load(fh)
    return str_1


def write_last_dict(request_comments: str, comments: dict):
    with open("database_2.json", "w") as fh:
        str_1 = {request_comments: comments}
        json.dump(str_1, fh, sort_keys=True, indent=2)


def read_last_dict() -> json:
    with open("database_2.json", "r") as fh:
        str_1 = json.load(fh)
    return str_1
