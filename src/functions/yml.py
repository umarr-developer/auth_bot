from yaml import safe_load


def read_yaml(filename: str) -> dict:
    with open(filename, mode='r', encoding='utf-8') as stream:
        return safe_load(stream)
