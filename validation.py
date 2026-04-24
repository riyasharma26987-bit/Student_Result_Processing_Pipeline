import pandas as pd
import logging
from config import SUBJECTS, MAX_MARKS


def validate(df: pd.DataFrame):
    valid = []
    invalid = []
    seen_rolls = set()

    for _, row in df.iterrows():
        errors = []

        # Check for duplicate roll number
        if row["roll_number"] in seen_rolls:
            errors.append("duplicate roll number")
        seen_rolls.add(row["roll_number"])

        # Check for missing marks
        for s in SUBJECTS:
            if pd.isna(row.get(s)):
                errors.append(f"missing mark: {s}")

        # Check for impossible marks
        for s in SUBJECTS:
            val = row.get(s)
            if not pd.isna(val):
                if val < 0 or val > MAX_MARKS[s]:
                    errors.append(f"invalid mark in {s}: {val}")

        if errors:
            logging.warning(f"Roll {row['roll_number']} rejected — {errors}")
            invalid.append({**row.to_dict(), "errors": str(errors)})
        else:
            valid.append(row.to_dict())

    print(f"[2] Validation complete — {len(valid)} valid, {len(invalid)} invalid records.")

    if invalid:
        print("    Invalid records:")
        for r in invalid:
            print(f"      Roll {r['roll_number']} — {r['errors']}")

    return pd.DataFrame(valid), invalid