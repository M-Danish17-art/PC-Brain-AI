import time

from collector import get_system_info
from database import create_database, save_metrics


INTERVAL_SECONDS = 30


def start_logger():

    create_database()

    print("=" * 55)
    print("              PC BRAIN AI")
    print("          AUTOMATIC SYSTEM LOGGER")
    print("=" * 55)
    print(f"Collection interval: {INTERVAL_SECONDS} seconds")
    print("Monitoring CPU, RAM, processes, drives, battery...")
    print("Press CTRL + C to stop.")
    print("=" * 55)

    record_number = 0

    try:

        while True:

            record_number += 1

            data = get_system_info()

            save_metrics(data)

            print(
                f"[{data['timestamp']}] "
                f"Record #{record_number} | "
                f"CPU: {data['cpu']['usage_percent']}% | "
                f"RAM: {data['memory']['usage_percent']}% | "
                f"Processes: {len(data['processes'])} | "
                f"Drives: {len(data['drives'])}"
            )

            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:

        print("\n")
        print("=" * 55)
        print("Logger stopped.")
        print(f"Records collected this session: {record_number}")
        print("=" * 55)


if __name__ == "__main__":
    start_logger()