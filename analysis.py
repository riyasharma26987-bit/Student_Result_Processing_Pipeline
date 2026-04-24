import pandas as pd
from config import SUBJECTS, PASS_MARK


def branch_toppers(df: pd.DataFrame) -> pd.DataFrame:
    toppers = df.loc[df.groupby("branch")["percentage"].idxmax()]
    return toppers[["branch", "rank", "name", "roll_number", "percentage", "grade"]].reset_index(drop=True)


def subject_failure_analysis(df: pd.DataFrame) -> dict:
    return {s: int((df[s] < PASS_MARK).sum()) for s in SUBJECTS}


def print_analysis(df: pd.DataFrame):
    print("\n" + "="*50)
    print("  ADVANCED ANALYSIS")
    print("="*50)

    print("\n--- Branch Toppers ---")
    toppers = branch_toppers(df)
    print(toppers.to_string(index=False))

    print("\n--- Subject Failure Count ---")
    failures = subject_failure_analysis(df)
    for subject, count in failures.items():
        print(f"  {subject:<15}: {count} student(s) failed")

    print("\n--- Overall Pass/Fail ---")
    passed = df["passed"].sum()
    failed = len(df) - passed
    print(f"  Passed: {passed}  |  Failed: {failed}")
    print("="*50)