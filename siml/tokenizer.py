from siml.tracer import Tracer
from siml.token import Token
from siml.token_types import TokenType, TOKEN_REGEX
from typing import Any, Dict

KEYWORDS = {
    "state",
    "config",
    "actions",
    "rules",
    "agents",
    "templates",
    "simulationd",
    "module",
    "import",
    "export"
    }

class Tokenizer:
    def __init__(self, source: str):
        self.lines = source.splitlines()
        self.tracer = Tracer("Tokenizer")
        self.keywords = KEYWORDS

    def __iter__(self):
        indent_width = 2    # Fixed indentation width of 2 spaces
        indent_stack = [0]  # Stack to track indentation levels

        for line, text in enumerate(self.lines, start=1):
            raw_indent = len(text) - len(text.lstrip())
            if raw_indent % indent_width != 0:
                raise SyntaxError(f"Indentation error on line {line}: not a multiple of {indent_width} spaces")

            indent_level = raw_indent // indent_width
            current_level = indent_stack[-1] 

            if indent_level > current_level:
                indent_stack.append(indent_level)
                token = Token(TokenType.INDENT, None, line, raw_indent)
                self.tracer.info(f"Tokenized: {token}")
                yield token

            elif indent_level < current_level:
                while indent_stack and indent_stack[-1] > indent_level:
                    indent_stack.pop()
                    token = Token(TokenType.DEDENT, None, line, indent_stack[-1] * 2)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

            # Remove inline comments and strip whitespace
            text = self.strip_inline_comment(text)
            if not text:  # Skip empty lines after stripping comments
                continue

            stripped = text.strip()
            if not stripped: # Skip empty lines
                continue
            
            yield from self._lex_line(stripped, line, raw_indent)

        # Handle any remaining dedents
        final_line = len(self.lines) + 1
        while len(indent_stack) > 1:
            indent_stack.pop()
            token = Token(TokenType.DEDENT, None, final_line, indent_stack[-1] * 2)
            self.tracer.info(f"Tokenized: {token}")
            yield token


    def _parse_token_value(self, value: str, token_type: TokenType, line: int) -> tuple[TokenType, Any]:
        """
        Parse the value of a token based on its type.
        Returns a tuple of (TokenType, value).
        - For NUMBER, it returns int or float based on the presence of a decimal point.
        - For STRING, it strips quotes.
        - For IDENTIFIER, it checks against keywords and returns appropriate TokenType.
        - For BOOLEAN, it converts "true" or "false" to boolean values.
        - For NULL, it returns None.
        - For other types, it returns the original token type and value.
        """
        match token_type:
            case TokenType.NUMBER:
                try:
                    return TokenType.NUMBER, float(value) if '.' in value else int(value)
                except ValueError:
                    raise SyntaxError(f"Invalid number format on line {line}: {value}")
                
            case TokenType.STRING:
                return TokenType.STRING, value.strip('"').strip("'")
            
            case TokenType.IDENTIFIER:
                if self.is_keyword(value):
                    return TokenType.KEYWORD, value
                
                elif value in ("true", "false"):
                    return TokenType.BOOLEAN, value == "true"
                
                elif value == "and":
                    return TokenType.AND, value
                
                elif value == "or":
                    return TokenType.OR, value
                
                elif value == "null":
                    return TokenType.NULL, None
                
                return TokenType.IDENTIFIER, value
            
            case _:
                return token_type, value

    def _lex_line(self, text: str, line: int, indent: int = 0):
        """
        Lex a single line of text into tokens.
        This method uses a regular expression to find all tokens in the line.
        It yields Token objects for each recognized token type.
        Assumes TOKEN_REGEX has been ordered to prioritize longest / more specific matches first.
        """
        for match in TOKEN_REGEX.finditer(text):
            kind = match.lastgroup
            value = match.group() 
            
            match kind:
                case "COLON":
                    token = Token(TokenType.COLON, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "DASH":
                    token = Token(TokenType.DASH, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "NUMBER":
                    token_type, token_value = self._parse_token_value(value, TokenType.NUMBER, line)
                    token = Token(token_type, token_value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "STRING":
                    token_type, token_value = self._parse_token_value(value, TokenType.STRING, line)
                    token = Token(token_type, token_value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "EQUAL_EQUAL":
                    token = Token(TokenType.EQUAL_EQUAL, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token
                
                case "NOT_EQUAL":
                    token = Token(TokenType.NOT_EQUAL, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "LESS_EQUAL":
                    token = Token(TokenType.LESS_EQUAL, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token
                
                case "GREATER_EQUAL":
                    token = Token(TokenType.GREATER_EQUAL, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "LPAREN":
                    token = Token(TokenType.LPAREN, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "RPAREN":
                    token = Token(TokenType.RPAREN, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "LBRACKET":
                    token = Token(TokenType.LBRACKET, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "RBRACKET":
                    token = Token(TokenType.RBRACKET, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token 

                case "COMMA":
                    token = Token(TokenType.COMMA, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "DOT": 
                    token = Token(TokenType.DOT, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "EQUALS":
                    token = Token(TokenType.EQUALS, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token 

                case "PLUS":
                    token = Token(TokenType.PLUS, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token
                case "MINUS":
                    token = Token(TokenType.MINUS, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "POWER":
                    token = Token(TokenType.POWER, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "MULTIPLY": 
                    token = Token(TokenType.MULTIPLY, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "DIVIDE":
                    token = Token(TokenType.DIVIDE, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "MODULO":
                    token = Token(TokenType.MODULO, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "LESS_THAN":
                    token = Token(TokenType.LESS_THAN, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "GREATER_THAN":
                    token = Token(TokenType.GREATER_THAN, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

                case "IDENTIFIER":
                    token_type, token_value = self._parse_token_value(value, TokenType.IDENTIFIER, line)
                    token = Token(token_type, token_value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

    def is_keyword(self, value: str) -> bool:
        return value in self.keywords
    
    def strip_inline_comment(self, line: str) -> str:
        """
        Strip inline comments from a line of text.
        Comments start with '#' and continue to the end of the line.
        Does not remove comments inside quotes.
        """
        if not line:
            return line
        
        stripped = []
        quote_char = None # Track what type of quote is currently open (single or double)
        for char in line:
            if char in ('"', "'"):
                if quote_char is None:
                    quote_char = char # Open a quote if not already in one
                elif quote_char == char:
                    quote_char = None # Close the quote if it matches the current one

            if char == '#' and quote_char is None:
                # If we hit a comment and we're not inside quotes, stop processing
                break

            stripped.append(char)

        return ''.join(stripped).rstrip()  # Remove trailing whitespace after stripping comments