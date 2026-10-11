
import csv
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"


def export_anomaly_report(anomalies):
    """Export detected anomalies to a timestamped CSV report."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"anomaly_report_{timestamp}.csv"

    fieldnames = [
        "record_id",
        "timestamp",
        "cpu_usage",
        "ram_usage",
        "disk_usage",
        "severity",
        "explanation",
    ]

    with report_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for anomaly in anomalies:
            writer.writerow(anomaly)

    return report_path

