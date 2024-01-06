from typing import Literal

from pydantic import dataclasses


@dataclasses.dataclass
class DBSpecification:
    """DB specification"""

    path: str
    engine: Literal["Default", "Postgres", "TinyDB"] = "Default"
