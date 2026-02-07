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
        score = max(partial, token)
        scores.append(score)

    return max(scores) if scores else 0

def is_low_signal(text: str) -> bool:
    words = text.split()

    if len(words) < 1:
        return True

    avg_word_len = sum(len(w) for w in words) / len(words)
    if avg_word_len > 10:
        return True

    return False


def route_domain(user_message: str):
    text = normalize(user_message)

    if is_low_signal(text):
        return {
            "domain": [],
            "status": "no_match"
        }

    scored_domains = []

    for domain in DOMAINS:
        if not domain.active:
            continue

        score = score_against_domain(text, domain)
        scored_domains.append((domain, score))

    scored_domains.sort(key=lambda x: x[1], reverse=True)

    STRONG_MATCH_THRESHOLD = 70
    WEAK_MATCH_THRESHOLD = 50
    TOP_DOMINANCE_GAP = 15

    top_domain, top_score = scored_domains[0]
    
    strong_matches = [
        {"domain": d.id, "score": s}
        for d, s in scored_domains
        if s >= STRONG_MATCH_THRESHOLD
    ]

    weak_matches = [
        {"domain": d.id, "score": s}
        for d, s in scored_domains
        if WEAK_MATCH_THRESHOLD <= s < STRONG_MATCH_THRESHOLD
    ]

    # --- decision logic ---

    # if strong_matches:
    #     return {
    #         "domain": strong_matches,
    #         "status": "confident"
    #     }
    if strong_matches:
        filtered = [
            m for m in strong_matches
            if top_score - m["score"] <= TOP_DOMINANCE_GAP
        ]

    return {
        "domain": filtered,
        "status": "confident"
    }


    if weak_matches:
        return {
            "domain": weak_matches,
            "status": "needs_clarification"
        }

    return {
        "domain": [],
        "status": "no_match"
    }
