import logging
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from env_variables_setup import initialize_spark

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    json_path = os.path.join(os.path.dirname(__file__), "pdi_servicenow_changes.json")

    if not os.path.exists(json_path):
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    try:
        initialize_spark()
        spark = SparkSession.builder \
            .appName("MockServiceNowChanges") \
            .master("local[*]") \
            .getOrCreate()

        df = spark.read.option("multiLine", True).json(json_path)

        filtered_df = (
            df.filter((col("risk") == "High") | (col("risk") == "Medium"))
              .select("number", "short_description", "risk")
        )

        filtered_df.show(truncate=False)

    except Exception as exc:
        print(f"Failed to process JSON data: {exc}")
        sys.exit(1)
    finally:
        if "spark" in locals():
            spark.stop()


if __name__ == "__main__":
    main()
