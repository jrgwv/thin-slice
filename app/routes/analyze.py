"""BFF layer — validates input, delegates to agent service, shapes response for frontend."""

import logging
import uuid

from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalyzeRequest, AnalyzeResponse
from app.services.agent_service import run_analysis

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    text = payload.text.strip()
    request_id = uuid.uuid4().hex[:12]

    if not text:
        raise HTTPException(status_code=400, detail="The 'text' field must not be empty.")

    if len(text) > 12000:
        raise HTTPException(status_code=400, detail="Input is too long for this prototype.")

    try:
        return run_analysis(request_id, text)
    except Exception as exc:
        logger.exception("request_id=%s — analysis failed", request_id)
        raise HTTPException(status_code=500, detail="Analysis failed.") from exc
