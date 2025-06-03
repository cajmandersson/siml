# SIML — Simulation Modeling Language

**SIML** is a declarative programming language for building agent-based simulations, synthetic data environments, and LLM-driven workflows. Designed for structured reasoning, training, and evaluation of autonomous agents, SIML combines YAML-style clarity with real-time event-driven behavior modeling.

## ✨ Features

- Declarative `state:`, `actions:`, `rules:`, `agents:`, and `synthesize:` sections
- Tick-based simulation loop with logging, tracing, and state mutation
- Structured `prompt:` and `result:` handling for LLM integration
- Agent support with context-based decision-making and action calling
- Portable syntax, CLI runner, and MCP-compatible runtime

## 🛠 Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/siml.git
cd siml
pip install -e .
```

Run a simulation:

```bash
siml run examples/hello_world.siml
```

## 📂 Project Structure

```
siml/
├── siml/               # core parser + runtime
├── cli/                # siml run, trace, etc.
├── examples/           # .siml programs
├── tests/              # unit tests
├── README.md
├── SIML_SPEC.md        # language reference
└── pyproject.toml
```

## 📄 License

Apache 2.0
