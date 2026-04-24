import pandas as pd
import logging


def ingest(filepath: str) -> pd.DataFrame:
    logging.info(f"Ingesting file: {filepath}")
    df = pd.read_csv(filepath)
    logging.info(f"Loaded {len(df)} raw records from {filepath}")
    print(f"[1] Ingestion complete — {len(df)} records loaded.")
    return df
