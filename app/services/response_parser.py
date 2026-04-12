import json
import re

from app.models.schemas import AnalyzeResponse


def _extract_json(raw_text: str) -> str:
    """Pull the first JSON object out of raw model output."""
    # Try stripping markdown fences first
    match = re.search(r"```(?:json)?\s*(\{.*?})\s*```", raw_text, re.DOTALL)
    if match:
        return match.group(1)
    # Fall back to first { ... }
    match = re.search(r"\{.*}", raw_text, re.DOTALL)
    if match:
        return match.group(0)
    return raw_text


def parse_model_output(raw_text: str) -> AnalyzeResponse:
    data = json.loads(_extract_json(raw_text))

    summary = str(data.get("summary", "")).strip()
    action_items = data.get("action_items", [])
    next_step = str(data.get("next_step", "")).strip()

    if not isinstance(action_items, list):
        action_items = []

    normalized_action_items = [str(item).strip() for item in action_items if str(item).strip()]

    return AnalyzeResponse(
        summary=summary or "No summary returned.",
        action_items=normalized_action_items[:5],
        next_step=next_step or "Review the result and refine the prototype.",
        raw_output=raw_text,
    )
