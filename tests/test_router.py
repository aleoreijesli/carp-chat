from app.domain.router import route_domain


def test_grading_only():
    result = route_domain("I have a grade of 85 can I still be a dean lister?")
    assert result["status"] == "confident"
    assert result["domain"][0]["domain"] == "GRADING"


def test_single_word_enrollment():
    result = route_domain("enrollment")
    assert result["status"] == "confident"
    assert result["domain"][0]["domain"] == "ENROLLMENT"


def test_memo_only():
    result = route_domain("memo")
    assert result["domain"][0]["domain"] == "MEMORANDUM"


def test_ambiguous_needs_clarification():
    result = route_domain("application")
    assert result["status"] in ["needs_clarification", "no_match"]
