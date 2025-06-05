from siml.tracer import Tracer
from siml.token import Token
from siml.token_types import TokenType, TOKEN_REGEX

KEYWORDS = {
    "state",
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


    def _lex_line(self, text: str, line: int, indent: int = 0):
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
                    token = Token(TokenType.NUMBER, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token
                case "STRING":
                    token = Token(TokenType.STRING, value.strip('"').strip("'"), line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token
                case "IDENTIFIER" if value in self.keywords:
                    token = Token(TokenType.KEYWORD, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token
                case "IDENTIFIER":
                    token = Token(TokenType.IDENTIFIER, value, line, indent)
                    self.tracer.info(f"Tokenized: {token}")
                    yield token

            
                
            
