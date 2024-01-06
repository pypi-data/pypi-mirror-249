from typing import Annotated

from pydantic import AfterValidator
from pydantic.dataclasses import dataclass
from typing_extensions import override

from .identifier import Identifier
from .pydantic_config import PYDANTIC_CONFIG as _PYDANTIC_CONFIG


def _validate_measure_name(name: str, /) -> str:
    assert "," not in name, "`,` is not allowed."
    assert name == name.strip(), "Leading or trailing whitespaces are not allowed."
    return name


@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class MeasureIdentifier(Identifier):  # pylint: disable=keyword-only-dataclass
    measure_name: Annotated[str, AfterValidator(_validate_measure_name)]

    @override
    def __repr__(self) -> str:
        return f"""m["{self.measure_name}"]"""
