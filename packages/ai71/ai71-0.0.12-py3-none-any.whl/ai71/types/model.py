import enum
from typing import Optional


class Model(str, enum.Enum):
    FALCON_180B = "tiiuae/falcon-180B-chat"


    @classmethod
    def _missing_(cls, value: object) -> Optional["Model"]:
        if not isinstance(value, str):
            return None
        value = value.lower()
        for member in cls:
            if member.lower() == value:
                return member
        return None