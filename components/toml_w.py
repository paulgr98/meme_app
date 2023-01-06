from datetime import date


def dumps(toml_dict, table="") -> str:
    document = []
    for key, value in toml_dict.items():
        match value:
            case dict():
                table_key = f"{table}.{key}" if table else key
                document.append(
                    f"\n[{table_key}]\n{dumps(value, table=table_key)}"
                )
            case _:
                document.append(f"{key} = {_dumps_value(value)}")
    return "\n".join(document)


def _dumps_value(value) -> str:
    match value:
        case bool():
            return_value = 'true' if value else 'false'
        case float() | int():
            return_value = str(value)
        case str():
            return_value = f"'{value}'"
        case date():
            return_value = value.isoformat()
        case list():
            return_value = f"[{', '.join(_dumps_value(v) for v in value)}]"
        case _:
            raise TypeError(
                f"{type(value).__name__} {value!r} is not supported"
            )
    return return_value
