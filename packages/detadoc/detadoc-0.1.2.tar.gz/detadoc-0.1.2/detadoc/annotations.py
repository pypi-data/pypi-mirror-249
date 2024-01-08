from __future__ import annotations

import re
from typing import Annotated

from pydantic import BeforeValidator, Field


def string_to_list(string: str|list) -> list:
    if not string:
        return list()
    if isinstance(string, str):
        return re.split(r'[\n;,]', string)
    return string


StringList = Annotated[list[str], BeforeValidator(string_to_list), Field(default_factory=list)]