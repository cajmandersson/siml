# SIML — Simulation Modeling Language

**SIML** is a declarative language for defining modular simulation environments, generating synthetic data, and training large language model (LLM) agents in structured, tick-based systems. It enables organizations to model production-like environments in isolated sandboxes for experimentation, traceability, and LLM-driven automation.

> This project is in early development. See [SIML_SPEC.md](./SIML_SPEC.md) for design goals and syntax.

---

## Use Case

SIML is designed for developers and domain experts to:

- Build structured data environments that simulate real-world systems
- Encode behaviors, rules, and side effects using declarative logic
- Simulate system dynamics over time to train or test LLM agents
- Export agent traces and rewards for fine-tuning or evaluation

---

## Key Features

- Modular top-level `simulation:` entry point
- Declarative `modules:` with local `state:`, `actions:`, `rules:`, and `templates:`
- Shared `agents:` that observe and act across module boundaries
- Synthetic data generation via `synthesize(template, count)`
- LLM function calling, contextual decision-making, and tick-based control
- CLI tools for running, tracing, and exporting simulations

---

## Program Layout

A complete SIML program has a single entry point:

```yaml
simulation:
  config:
    max_ticks: 10
    tick_unit: "days"

  agents:
    - agent: ...

  modules:
    - module:
        id: orders
        state: ...
        actions: ...
        rules: ...
        templates: ...

    - module: "./modules/invoicing.siml"
```

---

## Project Layout

```
siml/
├── siml/               # tokenizer, parser, runtime
├── cli/                # CLI commands
├── examples/           # complete .siml programs
├── tests/              # parser + runtime tests
├── README.md
├── SIML_SPEC.md        # language design
├── pyproject.toml
└── LICENSE
```

---

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/siml.git
cd siml
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run a SIML program:

```bash
siml run examples/invoice_simulation.siml
```

---

## Docs

- [SIML_SPEC.md](./SIML_SPEC.md) — full language spec and examples

---

## License

Apache 2.0 — open source and extensible. Contributions welcome.