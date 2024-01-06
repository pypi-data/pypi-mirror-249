import json

from src.utils.display import display_text


def pretty_print_dict(data: dict):
    display_text(json.dumps(data, indent=4))
