import statistics
from sklearn.ensemble import IsolationForest

from database import get_connection


# ============================================================
# LOAD METRICS
# ============================================================

def load_metrics():
    connection = get_connection()
    cursor = connection.cursor()

    rows = cursor.execute("""
        SELECT
            id,
            timestamp,
            cpu_usage,
            ram_usage,
            disk_usage
        FROM metrics
        ORDER BY id
    """).fetchall()

    connection.close()

    return rows


# ============================================================
# PERSONAL BASELINE
# ============================================================

def calculate_baseline(rows):
    cpu_values = [row[2] for row in rows]
    ram_values = [row[3] for row in rows]
    disk_values = [row[4] for row in rows]

    return {
        "cpu_avg": statistics.mean(cpu_values),
        "cpu_std": statistics.stdev(cpu_values) if len(cpu_values) > 1 else 0,

        "ram_avg": statistics.mean(ram_values),
        "ram_std": statistics.stdev(ram_values) if len(ram_values) > 1 else 0,

        "disk_avg": statistics.mean(disk_values),
        "disk_std": statistics.stdev(disk_values) if len(disk_values) > 1 else 0,
    }


# ============================================================
# ANOMALY EXPLANATION
# ============================================================

def explain_anomaly(cpu, ram, disk, baseline):

    explanations = []

    cpu_std = baseline["cpu_std"]
    ram_std = baseline["ram_std"]
    disk_std = baseline["disk_std"]

    if cpu_std > 0:
        cpu_z = (cpu - baseline["cpu_avg"]) / cpu_std

        if cpu_z >= 2:
            explanations.append(
                f"CPU usage is significantly above normal ({cpu:.1f}%)"
            )

    if ram_std > 0:
        ram_z = (ram - baseline["ram_avg"]) / ram_std

        if ram_z >= 2:
            explanations.append(
                f"RAM usage is significantly above normal ({ram:.1f}%)"
            )

    if disk_std > 0:
        disk_z = (disk - baseline["disk_avg"]) / disk_std

        if abs(disk_z) >= 2:
            explanations.append(
                f"Disk usage was unusual ({disk:.1f}%)"
            )

    if not explanations:
        explanations.append(
            "No single metric is extremely unusual."
        )

        explanations.append(
            "The combination of CPU, RAM and disk behavior "
            "was unusual for this dataset."
        )

    return explanations


# ============================================================
# SEVERITY
# ============================================================

def get_severity(cpu, ram, disk, baseline):

    z_scores = []

    if baseline["cpu_std"] > 0:
        z_scores.append(
            abs(
                (cpu - baseline["cpu_avg"])
                / baseline["cpu_std"]
            )
        )

    if baseline["ram_std"] > 0:
        z_scores.append(
            abs(
                (ram - baseline["ram_avg"])
                / baseline["ram_std"]
            )
        )

    if baseline["disk_std"] > 0:
        z_scores.append(
            abs(
                (disk - baseline["disk_avg"])
                / baseline["disk_std"]
            )
        )

    highest_z = max(z_scores) if z_scores else 0

    if highest_z >= 3:
        return "HIGH"

    if highest_z >= 2:
        return "MEDIUM"

    return "LOW"


# ============================================================
# LOAD PROCESS DATA
# ============================================================

def load_processes(metric_id):

    connection = get_connection()
    cursor = connection.cursor()

    rows = cursor.execute("""
        SELECT
            process_name,
            pid,
            cpu_percent,
            memory_percent
        FROM processes
        WHERE metric_id = ?
          AND process_name != 'System Idle Process'
          AND pid != 0
        ORDER BY cpu_percent DESC
    """, (metric_id,)).fetchall()

    connection.close()

    return rows


# ============================================================
# PROCESS CONTRIBUTOR SCORING
# ============================================================

def calculate_contributor_scores(processes):

    if not processes:
        return [], []

    # --------------------------------------------------------
    # CPU
    # --------------------------------------------------------

    cpu_total = sum(
        max(process[2], 0)
        for process in processes
    )

    cpu_contributors = []

    if cpu_total > 0:

        for name, pid, cpu, memory in processes:

            score = (max(cpu, 0) / cpu_total) * 100

            cpu_contributors.append({
                "name": name,
                "pid": pid,
                "cpu": cpu,
                "score": score
            })

    # --------------------------------------------------------
    # RAM
    # --------------------------------------------------------

    ram_total = sum(
        max(process[3], 0)
        for process in processes
    )

    ram_contributors = []

    if ram_total > 0:

        for name, pid, cpu, memory in processes:

            score = (max(memory, 0) / ram_total) * 100

            ram_contributors.append({
                "name": name,
                "pid": pid,
                "memory": memory,
                "score": score
            })

    # Highest contributor first
    cpu_contributors.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    ram_contributors.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return cpu_contributors, ram_contributors


# ============================================================
# SHOW PROCESS CORRELATION
# ============================================================

def show_process_contributors(metric_id):

    processes = load_processes(metric_id)

    if not processes:

        print()
        print("PROCESS CORRELATION")
        print("----------------------------------------")
        print("  No process data available.")

        return

    cpu_contributors, ram_contributors = (
        calculate_contributor_scores(processes)
    )

    print()
    print("PROCESS CORRELATION")
    print("----------------------------------------")

    # --------------------------------------------------------
    # CPU CONTRIBUTORS
    # --------------------------------------------------------

    print()
    print("CPU Contributors:")

    for contributor in cpu_contributors[:3]:

        print(
            f"  • {contributor['name']} "
            f"(PID {contributor['pid']}) — "
            f"CPU: {contributor['cpu']:.1f}% "
            f"| Relative contribution: "
            f"{contributor['score']:.1f}%"
        )

    # --------------------------------------------------------
    # RAM CONTRIBUTORS
    # --------------------------------------------------------

    print()
    print("RAM Contributors:")

    for contributor in ram_contributors[:3]:

        print(
            f"  • {contributor['name']} "
            f"(PID {contributor['pid']}) — "
            f"RAM: {contributor['memory']:.2f}% "
            f"| Relative contribution: "
            f"{contributor['score']:.1f}%"
        )


# ============================================================
# MAIN ML ANALYSIS
# ============================================================

def run_anomaly_detection():

    rows = load_metrics()

    if len(rows) < 10:

        print(
            "Not enough data for ML anomaly detection."
        )

        return

    baseline = calculate_baseline(rows)

    # --------------------------------------------------------
    # Dataset
    # --------------------------------------------------------

    X = [
        [
            row[2],  # CPU
            row[3],  # RAM
            row[4]   # Disk
        ]
        for row in rows
    ]

    # --------------------------------------------------------
    # Isolation Forest
    # --------------------------------------------------------

    model = IsolationForest(
        contamination=0.10,
        random_state=42
    )

    predictions = model.fit_predict(X)

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    print("=" * 70)
    print("                       PC BRAIN AI")
    print("          SMART ML + PROCESS ANALYSIS v0.6.4")
    print("=" * 70)

    print(f"Records analyzed : {len(rows)}")

    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    print()
    print("PERSONAL BASELINE")
    print("-" * 70)

    print(
        f"CPU  Average : "
        f"{baseline['cpu_avg']:.2f}%"
    )

    print(
        f"CPU  Std Dev : "
        f"{baseline['cpu_std']:.2f}%"
    )

    print(
        f"RAM  Average : "
        f"{baseline['ram_avg']:.2f}%"
    )

    print(
        f"RAM  Std Dev : "
        f"{baseline['ram_std']:.2f}%"
    )

    print(
        f"Disk Average : "
        f"{baseline['disk_avg']:.2f}%"
    )

    print(
        f"Disk Std Dev : "
        f"{baseline['disk_std']:.2f}%"
    )

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    print()
    print("ANOMALY RESULTS")
    print("-" * 70)

    anomaly_count = 0
    normal_count = 0

    for row, prediction in zip(rows, predictions):

        metric_id = row[0]
        timestamp = row[1]
        cpu = row[2]
        ram = row[3]
        disk = row[4]

        # ----------------------------------------------------
        # Normal
        # ----------------------------------------------------

        if prediction == 1:

            normal_count += 1

            continue

        # ----------------------------------------------------
        # Anomaly
        # ----------------------------------------------------

        anomaly_count += 1

        severity = get_severity(
            cpu,
            ram,
            disk,
            baseline
        )

        explanations = explain_anomaly(
            cpu,
            ram,
            disk,
            baseline
        )

        print()
        print(
            f"⚠ ANOMALY DETECTED — "
            f"Record #{metric_id}"
        )

        print(
            f"Time     : {timestamp}"
        )

        print(
            f"CPU      : {cpu:.1f}%"
        )

        print(
            f"RAM      : {ram:.1f}%"
        )

        print(
            f"Disk     : {disk:.1f}%"
        )

        print(
            f"Severity : {severity}"
        )

        print()
        print("Analysis:")

        for explanation in explanations:

            print(
                f"  • {explanation}"
            )

        # ----------------------------------------------------
        # Process analysis
        # ----------------------------------------------------

        show_process_contributors(
            metric_id
        )

       # --------------------------------------------------------
    # Smart Final Summary
    # --------------------------------------------------------

    high_count = 0
    medium_count = 0
    low_count = 0

    max_cpu = max(row[2] for row in rows)
    max_ram = max(row[3] for row in rows)
    max_disk = max(row[4] for row in rows)

    for row, prediction in zip(rows, predictions):

        if prediction == -1:
            severity = get_severity(
                row[2],
                row[3],
                row[4],
                baseline
            )

            if severity == "HIGH":
                high_count += 1
            elif severity == "MEDIUM":
                medium_count += 1
            else:
                low_count += 1

    print()
    print("=" * 70)
    print("                    SMART SYSTEM SUMMARY")
    print("=" * 70)

    print()
    print(f"Records analyzed : {len(rows)}")
    print(f"Anomalies        : {anomaly_count}")
    print(f"Normal records   : {normal_count}")

    print()
    print("Severity:")
    print(f"  HIGH   : {high_count}")
    print(f"  MEDIUM : {medium_count}")
    print(f"  LOW    : {low_count}")

    print()
    print("Highest Recorded Usage:")
    print(f"  CPU  : {max_cpu:.1f}%")
    print(f"  RAM  : {max_ram:.1f}%")
    print(f"  Disk : {max_disk:.1f}%")

    print()
    print("=" * 70)


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":
    run_anomaly_detection()