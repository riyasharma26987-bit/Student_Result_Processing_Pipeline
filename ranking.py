import pandas as pd
from config import SUBJECTS


def rank_students(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Tie-breaker: lower standard deviation = more consistent performance
    df["std_dev"] = df[SUBJECTS].std(axis=1).round(2)

    df = df.sort_values(
        by=["percentage", "std_dev"],
        ascending=[False, True]
    ).reset_index(drop=True)

    df["rank"] = df.index + 1

    print(f"[4] Ranking complete — {len(df)} students ranked.")
    return df