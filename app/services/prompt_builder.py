def build_prompt(user_text: str) -> str:
    return f"""You are helping turn rough notes into useful output.

Return the response in this exact JSON shape:
{{
  "summary": "short paragraph",
  "action_items": ["item 1", "item 2", "item 3"],
  "next_step": "single recommended next step"
}}

Rules:
- Be concise
- Keep action items practical
- Do not include markdown
- Return valid JSON only

Input:
{user_text}
""".strip()
