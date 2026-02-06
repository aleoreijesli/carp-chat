from fastapi import FastAPI
from pydantic import BaseModel
from app.domain.router import route_domain


app = FastAPI()

class DialogflowRequest(BaseModel):
    queryResult: dict

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/webhook")
async def dialogflow_webhook(body: DialogflowRequest):
    user_text = body.queryResult.get("queryText", "")

    routing = route_domain(user_text)

    status = routing["status"]
    domain = routing.get("domain", [])

    primary_domain = domain[0]["domain"] if domain else None

    print(
        "User said:", user_text,
        "domain:", domain,
        "status:", status
        )

    # Temporary responses per domain (stub handlers)
    if status == "confident":
        if primary_domain == "ENROLLMENT":
            reply = (
                "I can help you with enrollment concerns. "
                "Would you like to know about requirements, procedures, or deadlines?"
            )

        elif primary_domain == "SCHOLARSHIP":
            reply = (
                "I can assist you with scholarship-related questions. "
                "Are you looking for available scholarships or application requirements?"
            )

        elif primary_domain == "GRADING":
            reply = "I can help explain grading policies and GPA computation."

        elif primary_domain == "SCHEDULES":
            reply = "I can help you with class schedules and timetables."

        elif primary_domain == "ACADEMIC_POLICY":
            reply = "I can help explain academic policies and regulations."

        elif primary_domain == "MEMORANDUM":
            reply = "I can help summarize official memorandums and announcements."

        else:
            reply = (
                "I’m not entirely sure what topic this falls under yet. "
                "You can ask me about enrollment, scholarships, schedules, or policies."
            )

    elif status == "needs_clarification":
        reply = (
            "I want to make sure I understand correctly. "
            "Is your question about enrollment, scholarships, grading, schedules, "
            "academic policies, or memorandums?"
        )

    elif status == "multi_domain":
        domain_names = [d["domain"].replace("_", " ").title() for d in domain]

        reply = (
            f"I can help with multiple topics: {', '.join(domain_names)}. "
            "Which one would you like to discuss first?"
        )

    else:  # no_match
        reply = (
            "Sorry, I’m not sure I understood your question. "
            "Could you rephrase it or be more specific?"
        )

    return {
        "fulfillmentText": reply
    }