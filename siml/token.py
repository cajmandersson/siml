from dataclasses import dataclass 
from typing import Any
from siml.token_types import TokenType

@dataclass
class Token:
    type: TokenType
    value: Any
    line: int 
    indent: int
