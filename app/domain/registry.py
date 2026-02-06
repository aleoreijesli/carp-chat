from .models import Domain

DOMAINS = [
    Domain(
        id="ENROLLMENT",
        display_name="Enrollment",
        keywords=["enroll", "enrollment", "admission"],
        aliases=["apply", "register", "be in xu", "enter xu"]
    ),
    Domain(
        id="SCHOLARSHIP",
        display_name="Scholarship",
        keywords=["scholarship", "grant", "financial aid"],
        aliases=["tuition assistance", "study grant"]
    ),
    Domain(
        id="GRADING",
        display_name="Grading",
        keywords=["grade", "grading", "gpa", "marks"],
        aliases=["scores", "evaluation"]
    ),
    Domain(
        id="SCHEDULES",
        display_name="Schedules",
        keywords=["schedule", "class schedule", "timetable"],
        aliases=["class time", "subject time"]
    ),
    Domain(
        id="ACADEMIC_POLICY",
        display_name="Academic Policy",
        keywords=["policy", "academic policy", "rules"],
        aliases=["guidelines", "regulations"]
    ),
    Domain(
        id="MEMORANDUM",
        display_name="Memorandum",
        keywords=["memorandum", "memo", "announcement"],
        aliases=["notice", "official memo"]
    ),
]
