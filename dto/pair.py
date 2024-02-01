import pydantic
import typing as t


class Pair(pydantic.BaseModel):
    direction: str
    value: float
