
import sqlite3
import pandas as pd
import logging
from sqlalchemy import create_engine
from db_config import MYSQL_CONFIG


def save_to_sqlite(df: pd.DataFrame, db_path: str):
    conn = sqlite3.connect(db_path)
    df[["roll_number", "name", "branch"]].to_sql("students", conn, if_exists="replace", index=False)
    df[["roll_number", "total", "percentage", "gpa", "grade", "passed"]].to_sql("metrics", conn, if_exists="replace", index=False)
    df[["roll_number", "rank", "std_dev"]].to_sql("ranks", conn, if_exists="replace", index=False)
    conn.close()
    logging.info(f"SQLite: data saved to {db_path}")
    print(f"[6a] SQLite → {db_path}")


def save_to_mysql(df: pd.DataFrame):
    cfg = MYSQL_CONFIG
    url = f"mysql+pymysql://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}"
    engine = create_engine(url)
    try:
        with engine.connect() as conn:
            df[["roll_number", "name", "branch"]].to_sql("students", conn, if_exists="replace", index=False)
            df[["roll_number", "total", "percentage", "gpa", "grade", "passed"]].to_sql("metrics", conn, if_exists="replace", index=False)
            df[["roll_number", "rank", "std_dev"]].to_sql("ranks", conn, if_exists="replace", index=False)
        logging.info("MySQL: data saved successfully")
        print(f"[6b] MySQL → {cfg['database']} on {cfg['host']}")
    except Exception as e:
        logging.error(f"MySQL save failed: {e}")
        print(f"[6b] MySQL save FAILED: {e}")


def save_to_db(df: pd.DataFrame, db_path: str):
    save_to_sqlite(df, db_path)
    save_to_mysql(df)
