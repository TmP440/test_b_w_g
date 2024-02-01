import pydantic
import typing as t
from dto.pair import Pair


class Courses(pydantic.BaseModel):
    exchanger: t.Optional[str] = "binance"
    courses: t.List[Pair]
