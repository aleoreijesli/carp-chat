from app.domain.router import route_domain

def test_gibberish():
    result = route_domain("fjasdjfasd")
    assert result["status"] == "no_match"
    assert result["domain"][0]["domain"] == ""

def test_grading_only():
    result = route_domain("I have a grade of 85 can I still be a dean lister?")
    assert result["status"] == "confident"
    assert result["domain"][0]["domain"] == "GRADING"


def test_single_word_enrollment():
    result = route_domain("enrollment")
    assert result["status"] == "confident"
    assert result["domain"][0]["domain"] == "ENROLLMENT"

def test_enrollment_misspelt():
    result = route_domain("I'd like to enrol")
    assert result["status"] == "confident"
    assert result["domain"][0]["domain"] == "ENROLLMENT"

def test_enrollment_only():
    result = route_domain("I want to be in XU")
    assert result["status"] == "confident"
    assert result["domain"][0]["domain"] == "ENROLLMENT"

def test_memo_only():
    result = route_domain("memo")
    assert result["domain"][0]["domain"] == "MEMORANDUM"

def test_multi_domain():
    result = route_domain("Can you tell me about today's memo and university's admission?")
    assert result["domain"][0]["domain"] == "MEMORANDUM"
    assert result["domain"][1]["domain"] == "ENROLLMENT"

def test_ambiguous_needs_clarification():
    result = route_domain("application")
    assert result["status"] in ["needs_clarification", "no_match"]
