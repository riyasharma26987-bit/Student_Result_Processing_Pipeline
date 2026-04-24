import logging
import os

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

from pipeline import ingestion, validation, metrics, ranking, analysis, storage, output


def run():
    print("  STUDENT RESULT PROCESSING PIPELINE")

    # Stage 1: Ingest
    df_raw = ingestion.ingest("data/marks.csv")
    # Stage 2: Validate
    df_valid, df_invalid = validation.validate(df_raw)

    if df_valid.empty:
        print("No valid records to process. Exiting.")
        return

    # Stage 3: Compute metrics
    df_metrics = metrics.compute_metrics(df_valid)

    # Stage 4: Rank
    df_ranked = ranking.rank_students(df_metrics)

    # Stage 5: Analysis
    analysis.print_analysis(df_ranked)

    # Stage 6: Store in SQLite
    os.makedirs("db", exist_ok=True)
    storage.save_to_db(df_ranked, "db/results.db")

    # Stage 7: Generate outputs
    os.makedirs("output", exist_ok=True)
    output.export_csv(df_ranked, "output/results.csv")
    output.export_pdf(df_ranked, "output/merit_list.pdf")

    # Stage 8: Post-processing validation
    assert df_ranked["rank"].nunique() == len(df_ranked), "Duplicate ranks detected!"
    assert df_ranked["rank"].min() == 1, "Ranking does not start at 1!"
    logging.info("Post-processing validation passed.")
    print("\n[8] Post-processing validation passed.")

    

if __name__ == "__main__":
    run()