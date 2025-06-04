import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from siml.tracer import Tracer
from siml.tokenizer import Tokenizer


def main():
    Tracer.enabled = True

    source = '''
    state:
'''

    tokenizer = Tokenizer(source)
    tokenizer.tokenize()

if __name__ == "__main__":
    main()

