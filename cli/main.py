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
config:
  max_ticks: 10
  tick_unit: "days"

state:
  - invoices: synthesize(invoice_template, 100)
  - tick: 0

templates:
  - template: invoice_template
    examples:
      - id: 1
        amount: 4200
        status: "pending"

actions:
  - action: approve_invoice
    with: [invoice]
    do:
      - if invoice.amount < 5000:
          - set: invoice.status = "approved"
          - set: agent_reward = 1

rules:
  - trigger: on tick
    do:
      - for each: invoice in invoices
          - prompt agent: billing_agent with: invoice
      - set: tick = tick + 1

agents:
  - agent: "billing_agent"
    for each: invoice in invoices
    llm:
      provider: "openai"
      model: "gpt-4o"
      function_calling: true
    context:
      invoice: invoice
    can_call:
      - approve_invoice
'''
    tokenizer = Tokenizer(source)

    tokens = list(tokenizer)

if __name__ == "__main__":
    main()

