# GainesAI Thin Slice

A lean AI web app using FastAPI, structured with BFF and Observer patterns.
Powered by Amazon Bedrock (Claude Haiku 4.5) via the Converse API.

## What it does

Paste rough notes → get back a summary, action items, and a next step.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for full Mermaid diagrams.

```
Browser UI → FastAPI BFF → Agent Service → Bedrock (Converse API) → Structured JSON → UI
```

- **BFF layer** — validates input, delegates to agent service, shapes response for the frontend
- **Agent service** — orchestrates prompt → model → parse pipeline, emits observer events
- **Observer** — decoupled event system for logging, tracing, telemetry
- **Model layer** — Bedrock Converse API, model-agnostic (swappable)
- **Response parser** — extracts JSON from model output (handles markdown fences, preamble)

## Project structure

```
app/
  main.py                    # FastAPI entrypoint
  routes/
    analyze.py               # BFF — request handling
  services/
    agent_service.py          # orchestration + observer events
    ai_client.py              # model integration (Bedrock Converse API)
    prompt_builder.py         # prompt construction
    response_parser.py        # raw text → structured output
    observer.py               # event emitter/listener system
  models/
    schemas.py                # Pydantic request/response models
  static/
    index.html / app.js / styles.css
tests/
  test_parser.py
```

## Quick start

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` in the project root:

```env
DEMO_MODE=true
AWS_REGION=us-east-1
MODEL_ID=global.anthropic.claude-haiku-4-5-20251001-v1:0
```

Run:

```bash
./start.sh
# Open http://127.0.0.1:8000
```

## Modes

| Mode | Config | Behavior |
|------|--------|----------|
| Demo | `DEMO_MODE=true` (default) | Returns mock structured output |
| Live | `DEMO_MODE=false` | Calls Bedrock via Converse API |

Live mode requires AWS credentials with Bedrock access. The default model is the Claude Haiku 4.5 global inference profile — set `AWS_REGION` to a supported source region (us-east-1, us-west-2, etc.).

## Change isolation

| Want to...                    | Change only...         |
|-------------------------------|------------------------|
| Swap the model                | `ai_client.py`         |
| Change the prompt             | `prompt_builder.py`    |
| Add logging/tracing           | Register an observer   |
| Add a mobile frontend         | New BFF route          |
| Add tool calls or multi-step  | `agent_service.py`     |
| Change the response shape     | `response_parser.py`   |

## Docs

- [ARCHITECTURE.md](ARCHITECTURE.md) — Mermaid component + sequence diagrams
- [WALKTHROUGH.md](WALKTHROUGH.md) — Full code walkthrough: BFF pattern, Observer pattern, Converse API, JSON extraction
