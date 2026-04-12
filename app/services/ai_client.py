"""Model integration layer — sends prompt to model, returns raw text."""

import json
import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

_MOCK_RESPONSE = json.dumps({
    "summary": "This input describes an idea or set of notes that should be turned into a small, testable prototype before adding production complexity.",
    "action_items": [
        "Extract the main goal from the notes",
        "Build a small end-to-end demo",
        "Test the output with real sample input",
    ],
    "next_step": "Create the first working version and validate whether the output is actually useful.",
})


def call_model(prompt: str) -> str:
    """Send *prompt* to the model and return the raw response text."""
    if os.getenv("DEMO_MODE", "true").lower() == "true":
        return _MOCK_RESPONSE

    return _invoke_bedrock(prompt)


def _invoke_bedrock(prompt: str) -> str:
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("MODEL_ID", "global.anthropic.claude-haiku-4-5-20251001-v1:0")
    client = boto3.client("bedrock-runtime", region_name=region)

    try:
        response = client.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
        )
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Bedrock invocation failed: {exc}") from exc

    try:
        return response["output"]["message"]["content"][0]["text"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected model response format.") from exc
