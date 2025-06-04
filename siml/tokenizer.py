from siml.tracer import Tracer

class Tokenizer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tracer = Tracer("Tokenizer")

    def tokenize(self):
        self.tracer.info("Starting to Tokenize")
        self.tracer.debug(f"Source code length: {len(self.source_code)}")
        self.tracer.warn("This is a warning message during tokenization")
        self.tracer.failure("This is a failure message during tokenization")