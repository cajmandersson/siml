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
# this is a comment
  - users:
    - name: "Alice" # Including a comment
      age: 30.4
      hungry: .4
    - name: "#bob"
      age: -25
'''
    tokenizer = Tokenizer(source)

    tokens = list(tokenizer)

if __name__ == "__main__":
    main()

