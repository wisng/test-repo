from pydantic import ValidationError


def validate_data(data, dataclass):
    try:
        dto = dataclass(**data)
        return dto, None
    except ValidationError as e:
        return None, e.errors()
