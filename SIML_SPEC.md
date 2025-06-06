# SIML Specification — Draft (v0.2)

> SIML is a small declarative language and runtime designed for:
> - Defining simulation environments
> - Running tick-based simulations
> - Training and evaluating LLM-based autonomous agents

---

## What SIML Is

SIML is a YAML-like DSL for building simulations where:
- You define structured state via `state:` blocks
- Encode behaviors with `actions:` and `rules:`
- Create reusable data patterns using `templates:`
- Register agents that call actions via `agents:`
- Compose modules into a simulation using `simulation:`
- Run time-based logic over discrete ticks
- Collect logs and rewards to train or evaluate agents

---

## What SIML Does

| Feature            | Description |
|--------------------|-------------|
| Define State     | Describe your world with nested variables |
| Define Behavior  | Create actions and triggers that run at each tick |
| Run Simulations  | SIML executes modules step-by-step, deterministically |
| Prompt Agents    | LLMs observe structured state and choose actions |
| Log and Reward   | Track what happens each tick; log rewards |
| Export Datasets  | Convert simulations into datasets for fine-tuning |
| Modular Design   | Compose behavior from reusable building blocks |
| Import Logic     | Import templates, actions, and rules from other files |

---

## Entry Point

Every SIML program starts from a `simulation:` block.

```yaml
simulation:
  config:
    max_ticks: 30
    tick_unit: "days"
  agents:
    - agent: ...
  modules:
    - ./modules/invoice.siml
    - module:
        id: orders
        state:
          ...
        actions:
          ...
```

---

## Top-Level Blocks

```yaml
simulation:  # Root of the SIML program

config:      # Simulation time config (inside simulation)
agents:      # Global agent definitions
modules:     # A list of imported or inline module definitions
```

---

## Inside a Module

A module is a self-contained unit of state and logic.

```yaml
module:
  id: invoice_module
  state:
    ...
  actions:
    ...
  rules:
    ...
  templates:
    ...
```

---

## Cross-File Composition

You can break up logic into reusable files and import them.

```yaml
# actions.siml
export action:
  name: approve_invoice
  with: [invoice]
  do:
    - set: invoice.status = "approved"

# templates.siml
export template:
  name: invoice_template
  examples:
    - id: 1
      amount: 1000
      status: "pending"

# main.siml
simulation:
  config:
    max_ticks: 20
    tick_unit: "hours"
  modules:
    - module:
        id: invoices
        import:
          - ./actions.siml
          - ./templates.siml
        state:
          - invoices: synthesize(invoice_template, 100)
        rules:
          ...
```

---

## Agent Block

Agents observe state and can call declared actions.

```yaml
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
```

---
## Example Module
```yaml
module:
  id: support_module

  state:
    - users:
        - id: 1
          profile:
            name: "Alice"
            role: "customer"
            address:
              street: "Main St"
              city: "Metropolis"
              country: "Fictionland"
            preferences:
              notifications:
                email: true
                sms: false
        - id: 2
          profile:
            name: "Bob"
            role: "agent"
            address:
              street: "Second St"
              city: "Metropolis"
              country: "Fictionland"
            preferences:
              notifications:
                email: true
                sms: true

    - support_queue:
        open:
          - ticket_id: 101
            status: "new"
            assigned_to: null
            customer_id: 1
            messages:
              - from: "Alice"
                content: "I can't log in."
                timestamp: 0
        closed: []

    - settings:
        working_hours:
          start: 9
          end: 17
        escalation_threshold: 2
        auto_assign_enabled: true

  actions:
    - action: assign_ticket
      with: [ticket]
      do:
        - set: ticket.assigned_to = "agent:42"

  rules:
    - trigger: on tick
      do:
        - for each: ticket in support_queue.open
            - if ticket.assigned_to == null:
                - call: assign_ticket with: ticket
```

## Notes

- Each module should define a unique `id`
- Modules can **import** shared definitions like actions, templates, or rules
- You can define **inline** or **external** modules and mix both
- Agents live outside modules but observe and act on module state

---

## What's Out of Scope

- Arbitrary Python execution
- UI-based modeling
- Turing-complete logic
- Tight coupling between modules (must use signals/actions)

---

## Summary

SIML helps you:

1. Model dynamic state over time
2. Train agents in structured simulations
3. Encourage modular, composable DSL design
4. Export logs and datasets to train real LLM agents
