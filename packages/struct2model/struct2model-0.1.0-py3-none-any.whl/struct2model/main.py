from datetime import datetime
import re
from typing import Any


def get_value_from_path(obj: dict[str, Any], path: str):
    if "." in path:
        key, rest = path.split(".", 1)
        return get_value_from_path(obj[key], rest)
    else:
        return obj[path]


FUNCTION_REGEX = re.compile(r"(\w+)(:?,(.+))")

FUNCTION_ARGS_REGEX = re.compile(r"([^,]+)")


def func_date(value: str, format_: str):
    return datetime.strptime(value, format_).date()


def func_datetime(value: str, format_: str):
    return datetime.strptime(value, format_)


def func_bool(value: str, true_value: str):
    return value == true_value


FUNCTIONS = {
    "date": func_date,
    "bool": func_bool,
    "datetime": func_datetime,
}


def evaluate_function(func_name: str, value: Any, args: list[str]):
    func = FUNCTIONS[func_name]
    return func(value, *args)


def transform_value(
    obj: dict[str, Any], rules: dict[str, Any]
):  # -> Any | dict[str, Any]:
    if isinstance(rules, str):
        if "|" in rules:
            path, func_data = rules.split("|", 1)

            func_match = FUNCTION_REGEX.match(func_data)
            func_name, _, func_args = func_match.groups()

            func_args_match: list[str] = FUNCTION_ARGS_REGEX.findall(func_args)

            args: list[str] = []
            current_arg = ""
            for arg in func_args_match:
                if arg.startswith("'"):
                    current_arg = arg[1:]
                elif arg.endswith("'"):
                    args.append(current_arg + "," + arg[:-1])
                    current_arg = ""
                elif current_arg:
                    current_arg += arg
                else:
                    args.append(arg)

            if current_arg:
                args.append(current_arg)

            value = get_value_from_path(obj, path)
            return evaluate_function(func_name, value, args)

        return get_value_from_path(obj, rules)
    elif isinstance(rules, dict):
        if "__for__" in rules:
            for_key = rules["__for__"]
            as_key = rules["__as__"]

            value_to_iterate = get_value_from_path(obj, for_key)

            return [
                transform_value(
                    {as_key: value},
                    {
                        key: value
                        for key, value in rules.items()
                        if key not in ["__for__", "__as__"]
                    },
                )
                for value in value_to_iterate
            ]
        return {key: transform_value(obj, value) for key, value in rules.items()}
