import pydantic
import typing
from dto.pair import Pair


class Courses(pydantic.BaseModel):
    exchange: typing.Optional[str]
    courses: typing.List[Pair]
