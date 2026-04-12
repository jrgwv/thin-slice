from app.services.response_parser import parse_model_output


def test_parse_clean_json():
    raw = '{"summary":"hello","action_items":["a","b"],"next_step":"ship it"}'
    result = parse_model_output(raw)
    assert result.summary == "hello"
    assert result.action_items == ["a", "b"]
    assert result.next_step == "ship it"


def test_parse_markdown_fenced_json():
    raw = 'Here is the result:\n```json\n{"summary":"fenced","action_items":["x"],"next_step":"go"}\n```'
    result = parse_model_output(raw)
    assert result.summary == "fenced"
    assert result.action_items == ["x"]
    assert result.next_step == "go"


def test_parse_json_with_preamble():
    raw = 'Sure, here you go:\n{"summary":"preamble","action_items":[],"next_step":"next"}'
    result = parse_model_output(raw)
    assert result.summary == "preamble"
    assert result.next_step == "next"


def test_parse_missing_fields_uses_defaults():
    raw = '{"summary":"","action_items":[],"next_step":""}'
    result = parse_model_output(raw)
    assert result.summary == "No summary returned."
    assert result.next_step == "Review the result and refine the prototype."


def test_parse_bare_fences():
    raw = '```\n{"summary":"bare","action_items":["a"],"next_step":"done"}\n```'
    result = parse_model_output(raw)
    assert result.summary == "bare"
