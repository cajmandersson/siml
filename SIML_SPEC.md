# SIML Language Specification (v1)

## 1. Top-Level Sections

- `state:` – define simulation and agent state
- `actions:` – define callable side-effecting logic
- `rules:` – tick- or event-triggered logic blocks
- `agents:` – LLM-based agents that observe state and choose actions
- `synthesize_templates:` – LLM-driven data generators
- `import:` – multi-file program composition

## 2. Execution Model

1. At each tick:
   - Apply `rules:` (if triggered)
   - Execute LLM `agents:` (prompt + result)
   - Process `emit:` events
   - Log all state changes
   - Increment `tick`

## 3. Core Keywords

- `set:`, `log:`, `emit:`, `do:`, `if`, `for each:`, `prompt:`, `result.*`, `append to:`

## 4. Agent Behavior

Agents are defined per entity (`for each`) and are triggered by rules. They observe structured context and call declared `actions:` (functions) via LLM tool-calling.

## 5. MCP Compatibility

Every `action:` is MCP-exportable as a function/tool with input schema. AgentOps exposes these via the MCP Remote API for OpenAI integration.
