import logging
import os
import subprocess
import sys
from pathlib import Path


def configure_logging(log_file: Path) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, encoding="utf-8"),
        ],
    )


def run_script(script_path: Path) -> int:
    logging.info("Starting script: %s", script_path.name)

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8:replace"
    env["PYTHONUTF8"] = "1"

    process = subprocess.Popen(
        [sys.executable, str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        env=env,
    )

    assert process.stdout is not None

    for line in process.stdout:
        line = line.rstrip("\n")
        if line:
            logging.info("[%s] %s", script_path.name, line)

    process.stdout.close()
    return_code = process.wait()
    logging.info("Script finished: %s with exit code %d", script_path.name, return_code)
    return return_code


def main() -> int:
    root_dir = Path(__file__).resolve().parent
    log_file = root_dir / "pipeline_execution.log"
    configure_logging(log_file)

    scripts = [
        root_dir / "fetch_sn_data.py",
        root_dir / "read_pdi_servicenow_pyspark.py",
        root_dir / "run_itsm_agentsV2.py",
    ]

    for script_path in scripts:
        if not script_path.exists():
            logging.error("Missing script file: %s", script_path)
            return 1

        return_code = run_script(script_path)
        if return_code != 0:
            logging.error(
                "Pipeline stopped because %s exited with non-zero status %d",
                script_path.name,
                return_code,
            )
            return return_code

    logging.info("Pipeline completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
