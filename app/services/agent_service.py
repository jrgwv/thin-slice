"""Agent Service — orchestration layer between BFF and model integration."""

import logging

from app.models.schemas import AnalyzeResponse
from app.services import observer
from app.services.ai_client import call_model
from app.services.prompt_builder import build_prompt
from app.services.response_parser import parse_model_output

logger = logging.getLogger(__name__)


def run_analysis(request_id: str, user_text: str) -> AnalyzeResponse:
    """Orchestrate prompt → model → parse, emitting observer events at each stage."""

    observer.emit("agent:start", {"request_id": request_id})

    prompt = build_prompt(user_text)
    observer.emit("agent:prompt_built", {"request_id": request_id, "prompt_len": len(prompt)})

    raw = call_model(prompt)
    observer.emit("agent:model_returned", {"request_id": request_id, "raw_len": len(raw)})

    result = parse_model_output(raw)
    observer.emit("agent:complete", {"request_id": request_id, "summary_len": len(result.summary)})

    return result
