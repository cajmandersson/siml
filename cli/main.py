import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from siml.tracer import Tracer
from siml.tokenizer import Tokenizer

from siml.ast_nodes import (
    SimulationNode, ModuleNode, StateVarNode, NumberNode
)


def main():
    Tracer.enabled = True

    source = '''
state:
config:
  max_ticks: 10
  tick_unit: "days"

state:
  - invoices: generate(invoice_template, 100)
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

    # Build a small fake AST manually
    fake_ast = SimulationNode(
        line=1,
        indent=0,
        modules=[
            ModuleNode(
                line=2,
                indent=2,
                name="core",
                state=[
                    StateVarNode(
                        line=3,
                        indent=4,
                        name="tick",
                        value=NumberNode(line=3, indent=6, value=0)
                    )
                ]
            )
        ]
    )

    tracer = Tracer("AST")
    tracer.enabled = True
    tracer.debug_ast(fake_ast)

if __name__ == "__main__":
    main()

