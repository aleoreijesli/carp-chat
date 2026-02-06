import re
from rapidfuzz import fuzz
from .registry import DOMAINS


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def score_against_domain(text: str, domain) -> int:
    scores = []

    for keyword in domain.keywords + domain.aliases:
        partial = fuzz.partial_ratio(text, keyword)
        token = fuzz.token_set_ratio(text, keyword)

        # weighted blend
        score = max(partial, token)
        scores.append(score)

    return max(scores) if scores else 0


def is_low_signal(text: str) -> bool:
    words = text.split()

    # too short
    if len(words) < 2:
        return True

    # gibberish ratio
    avg_word_len = sum(len(w) for w in words) / len(words)
    if avg_word_len > 12:
        return True

    return False


def route_domain(user_message: str):
    text = normalize(user_message)

    if is_low_signal(text):
        return {
            "domain": "UNKNOWN",
            "confidence": 0,
            "status": "no_match"
        }

    scored_domains = []

    for domain in DOMAINS:
        if not domain.active:
            continue

        score = score_against_domain(text, domain)
        scored_domains.append((domain, score))

    scored_domains.sort(key=lambda x: x[1], reverse=True)

    STRONG_MATCH_THRESHOLD = 65

    strong_matches = [
        {"domain": d.id, "score": s}
        for d, s in scored_domains
        if s >= STRONG_MATCH_THRESHOLD
    ]

    if len(strong_matches) == 1:
        domain = strong_matches[0]
        return {
            "domain": [domain],
            "status": "confident"
        }

    return {
        "domain": strong_matches,
        "status": "multi_domain"
    }
