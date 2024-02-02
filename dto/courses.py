import pydantic
import typing as t
from dto.pair import Pair


class Courses(pydantic.BaseModel):
    exchange: t.Optional[str]
    courses: t.List[Pair]
