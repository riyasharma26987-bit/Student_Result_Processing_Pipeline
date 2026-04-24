import pandas as pd
from config import SUBJECTS, PASS_MARK, GRACE_MARKS, get_grade, get_gpa


def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Apply grace marks: if student failed by <= GRACE_MARKS, bump to pass
    for s in SUBJECTS:
        df[s] = df[s].apply(
            lambda x: min(x + GRACE_MARKS, 100)
            if x < PASS_MARK and x >= (PASS_MARK - GRACE_MARKS)
            else x
        )

    df["total"]      = df[SUBJECTS].sum(axis=1)
    df["percentage"] = (df["total"] / (len(SUBJECTS) * 100)) * 100
    df["percentage"] = df["percentage"].round(2)
    df["gpa"]        = df["percentage"].apply(get_gpa)
    df["grade"]      = df["percentage"].apply(get_grade)
    df["passed"]     = df[SUBJECTS].apply(lambda row: all(row >= PASS_MARK), axis=1)

    print(f"[3] Metrics computed for {len(df)} students.")
    return df