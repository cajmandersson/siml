from enum import Enum
import re 

class TokenType(Enum):
    KEYWORD = 1
    COLON = 2
    DASH = 3
    IDENTIFIER = 4
    NUMBER = 5
    STRING = 6
    INDENT = 7
    DEDENT = 8

TOKEN_REGEX = re.compile(r'''
    (?P<COLON>:)
    | (?P<DASH>-)
    | (?P<NUMBER>\d+)
    | (?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_]*)
    | (?P<STRING>"[^"]*"|'[^']*')

''', re.VERBOSE)