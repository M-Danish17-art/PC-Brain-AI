import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "pc_brain.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def get_basic_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    result = cursor.execute("""
        SELECT
            COUNT(*),
            AVG(cpu_usage),
            MIN(cpu_usage),
            MAX(cpu_usage),
            AVG(ram_usage),
            MIN(ram_usage),
            MAX(ram_usage),
            AVG(disk_usage),
            MIN(disk_usage),
            MAX(disk_usage)
        FROM metrics
    """).fetchone()

    connection.close()

    return {
        "total_records": result[0],

        "cpu": {
            "average": result[1],
            "minimum": result[2],
            "maximum": result[3]
        },

        "ram": {
            "average": result[4],
            "minimum": result[5],
            "maximum": result[6]
        },

        "disk": {
            "average": result[7],
            "minimum": result[8],
            "maximum": result[9]
        }
    }


def get_process_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    result = cursor.execute("""
        SELECT
            process_name,
            COUNT(*) AS occurrences,
            AVG(cpu_percent) AS avg_cpu,
            AVG(memory_percent) AS avg_memory
        FROM processes
        WHERE process_name != 'System Idle Process'
        GROUP BY process_name
        ORDER BY avg_memory DESC
        LIMIT 10
    """).fetchall()
    connection.close()

    return result


def get_drive_statistics():

    connection = get_connection()
    cursor = connection.cursor()

    result = cursor.execute("""
        SELECT
            drive_letter,
            AVG(usage_percent) AS avg_usage,
            MIN(free_gb) AS minimum_free_gb,
            MAX(free_gb) AS maximum_free_gb
        FROM drives
        GROUP BY drive_letter
        ORDER BY drive_letter
    """).fetchall()

    connection.close()

    return result


def print_report():

    statistics = get_basic_statistics()

    print()
    print("=" * 60)
    print("                 PC BRAIN AI")
    print("              DATA ANALYSIS REPORT")
    print("=" * 60)

    print()
    print("SYSTEM SNAPSHOTS")
    print("-" * 60)
    print(f"Total records: {statistics['total_records']}")

    print()
    print("CPU")
    print("-" * 60)
    print(f"Average : {statistics['cpu']['average']:.2f}%")
    print(f"Minimum : {statistics['cpu']['minimum']:.2f}%")
    print(f"Maximum : {statistics['cpu']['maximum']:.2f}%")

    print()
    print("RAM")
    print("-" * 60)
    print(f"Average : {statistics['ram']['average']:.2f}%")
    print(f"Minimum : {statistics['ram']['minimum']:.2f}%")
    print(f"Maximum : {statistics['ram']['maximum']:.2f}%")

    print()
    print("C: DRIVE")
    print("-" * 60)
    print(f"Average usage : {statistics['disk']['average']:.2f}%")
    print(f"Minimum usage : {statistics['disk']['minimum']:.2f}%")
    print(f"Maximum usage : {statistics['disk']['maximum']:.2f}%")

    print()
    print("TOP PROCESSES BY AVERAGE MEMORY")
    print("-" * 60)

    processes = get_process_statistics()

    for name, occurrences, avg_cpu, avg_memory in processes:
        print(
            f"{name:<25} "
            f"RAM: {avg_memory:>6.2f}% | "
            f"CPU: {avg_cpu:>6.2f}%"
        )

    print()
    print("DRIVE STATISTICS")
    print("-" * 60)

    drives = get_drive_statistics()

    for drive, avg_usage, min_free, max_free in drives:
        print(
            f"{drive:<5} "
            f"Avg Usage: {avg_usage:>6.2f}% | "
            f"Free: {min_free:.2f} - {max_free:.2f} GB"
        )

    print()
    print("=" * 60)
    print("Analysis complete.")
    print("=" * 60)


if __name__ == "__main__":
    print_report()