SUBJECTS = ["math", "physics", "chemistry", "english", "programming"]

MAX_MARKS = {s: 100 for s in SUBJECTS}

PASS_MARK = 40

GRACE_MARKS = 5


GRADE_SCALE = [
    (90, "A+"),
    (80, "A"),
    (70, "B"),
    (60, "C"),
    (50, "D"),
    (0,  "F"),
]


def get_grade(percentage):
    for threshold, grade in GRADE_SCALE:
        if percentage >= threshold:
            return grade
    return "F"


def get_gpa(percentage):
    if percentage >= 90: return 10.0
    if percentage >= 80: return 9.0
    if percentage >= 70: return 8.0
    if percentage >= 60: return 7.0
    if percentage >= 50: return 6.0
    return 0.0