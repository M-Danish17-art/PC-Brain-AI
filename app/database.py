import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "pc_brain.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Main system metrics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            cpu_usage REAL,
            cpu_frequency REAL,
            ram_usage REAL,
            ram_used_gb REAL,
            ram_available_gb REAL,
            disk_usage REAL,
            disk_used_gb REAL,
            disk_free_gb REAL,
            battery_percent REAL,
            battery_plugged INTEGER,
            network_sent INTEGER,
            network_received INTEGER
        )
    """)

    # Process monitoring table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_id INTEGER,
            process_name TEXT,
            pid INTEGER,
            cpu_percent REAL,
            memory_percent REAL,
            FOREIGN KEY(metric_id) REFERENCES metrics(id)
        )
    """)

    # Drive monitoring table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_id INTEGER,
            drive_letter TEXT,
            total_gb REAL,
            used_gb REAL,
            free_gb REAL,
            usage_percent REAL,
            FOREIGN KEY(metric_id) REFERENCES metrics(id)
        )
    """)

    connection.commit()
    connection.close()


def save_metrics(data):
    connection = get_connection()
    cursor = connection.cursor()

    battery = data["battery"]

    # Save main system metrics
    cursor.execute("""
        INSERT INTO metrics (
            timestamp,
            cpu_usage,
            cpu_frequency,
            ram_usage,
            ram_used_gb,
            ram_available_gb,
            disk_usage,
            disk_used_gb,
            disk_free_gb,
            battery_percent,
            battery_plugged,
            network_sent,
            network_received
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["cpu"]["usage_percent"],
        data["cpu"]["frequency_mhz"],
        data["memory"]["usage_percent"],
        data["memory"]["used_gb"],
        data["memory"]["available_gb"],
        data["disk"]["usage_percent"],
        data["disk"]["used_gb"],
        data["disk"]["free_gb"],
        battery["percentage"],
        int(battery["plugged_in"])
        if battery["plugged_in"] is not None else None,
        data["network"]["bytes_sent"],
        data["network"]["bytes_received"]
    ))

    # Get ID of the system snapshot
    metric_id = cursor.lastrowid

    # Save processes
    for process in data.get("processes", []):
        cursor.execute("""
            INSERT INTO processes (
                metric_id,
                process_name,
                pid,
                cpu_percent,
                memory_percent
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            metric_id,
            process["name"],
            process["pid"],
            process["cpu_percent"],
            process["memory_percent"]
        ))

    # Save drives
    for drive in data.get("drives", []):
        cursor.execute("""
            INSERT INTO drives (
                metric_id,
                drive_letter,
                total_gb,
                used_gb,
                free_gb,
                usage_percent
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            metric_id,
            drive["letter"],
            drive["total_gb"],
            drive["used_gb"],
            drive["free_gb"],
            drive["usage_percent"]
        ))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
    print(f"Location: {DATABASE_PATH}")