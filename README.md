# SIML — Simulation Modeling Language

**SIML** is a declarative programming language for building agent-based simulations, synthetic data environments, and LLM-driven workflows. Designed for structured reasoning, training, and evaluation of autonomous agents, SIML combines YAML-style clarity with real-time event-driven behavior modeling.

> This project is in early development. See [SIML_SPEC.md](./SIML_SPEC.md) for design goals and syntax plans.

---

## Features (Planned)

- Declarative `state:`, `actions:`, `rules:`, `agents:`, and `templates:` blocks
- Support for nested data structures (lists, dicts, primitives)
- Tick-based simulation runtime with state diffs, logging, and reward attribution
- LLM-powered agents with structured function calling and per-instance memory
- Synthetic data generation using `synthesize(template, count)`
- CLI tools: `siml run`, `siml trace`, `siml export`
- MCP-compatible: export agents and tools for OpenAI / remote use
- Local + API-based runtime support (bring your own OpenAI key)

---

## Project Layout

```
siml/
├── siml/               # core parser + runtime (TBD)
├── cli/                # CLI commands (TBD)
├── examples/           # .siml programs
├── tests/              # unit tests (TBD)
├── README.md
├── SIML_SPEC.md        # language design (draft)
├── pyproject.toml
└── LICENSE
```

---

## Getting Started (Dev Mode)

```bash
git clone https://github.com/YOUR_USERNAME/siml.git
cd siml
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run a CLI command (once implemented):

```bash
siml run examples/hello_world.siml
```

---

## Docs & Design

- [SIML_SPEC.md](./SIML_SPEC.md) — high-level overview, semantics, examples

---

## License

Apache 2.0 — open source and extensible.
