# SIML Specification — Draft (v0.1)

> SIML is a small declarative language and runtime designed for:
> - Defining simulation environments
> - Running tick-based simulations
> - Training and evaluating LLM-based autonomous agents

---

## What SIML Is

SIML is a YAML-like DSL for building simulations where:
- You define structured state (`state:`)
- Define logic and side effects via `actions:` and `rules:`
- Declare autonomous `agents:` that observe state and call actions
- Generate synthetic data using `templates:` + `synthesize()`
- Simulate the system over discrete time steps (ticks)
- Track outcomes, log events, and collect reward signals
- Export traces and datasets for training or evaluating agents

---

## What SIML Does

| Feature            | Description |
|--------------------|-------------|
| Define State     | You describe your world with nested variables |
| Define Behavior  | You define actions (`do:`) and triggers (`rules:`) |
| Run Simulations  | SIML executes step-by-step ticks with deterministic state transitions |
| Prompt Agents    | LLM agents observe state and call declared tools |
| Log and Reward   | Each tick is logged; rewards are assigned for training |
| Export Datasets  | You can export training-ready JSONL datasets |
| Support OpenAI   | The runtime can call real models with your API key |
| Run Locally      | SIML is CLI-based and open source |

---

## Top-Level Blocks

```yaml
config:      # simulation length, units, randomness
state:       # starting values
actions:     # things that mutate the state
rules:       # logic that triggers each tick
agents:      # LLMs that act in the simulation
templates:   # data generators for synthesized state
```

---

## Example

```yaml
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
  - agent: billing_agent
    for each: invoice in invoices
    llm:
      provider: openai
      model: gpt-4o
      function_calling: true
    context:
      invoice: invoice
    can_call:
      - approve_invoice
```

---

## What's Out of Scope

- General-purpose computation
- UI-based programming
- Arbitrary Python code injection

---

## Summary

SIML helps you:

1. Model dynamic state
2. Encode agent behavior
3. Simulate what agents would do
4. Export the data you need to train and evaluate them


