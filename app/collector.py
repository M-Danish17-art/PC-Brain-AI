import psutil
import platform
from datetime import datetime


def get_processes():
    processes = []

    # First measurement: initialize CPU counters
    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            if process.info["pid"] == 0:
                continue

            if process.info["name"] == "System Idle Process":
                continue

            process.cpu_percent(None)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Short measurement interval
    psutil.cpu_percent(interval=0.5)

    # Second measurement
    for process in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            pid = process.info["pid"]
            name = process.info["name"]

            # Ignore System Idle Process
            if pid == 0 or name == "System Idle Process":
                continue

            cpu = process.cpu_percent(None)
            memory = process.info["memory_percent"] or 0.0

            processes.append({
                "name": name or "Unknown",
                "pid": pid,
                "cpu_percent": round(cpu, 2),
                "memory_percent": round(memory, 2)
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Highest CPU processes
    top_cpu = sorted(
        processes,
        key=lambda x: x["cpu_percent"],
        reverse=True
    )[:5]

    # Highest memory processes
    top_memory = sorted(
        processes,
        key=lambda x: x["memory_percent"],
        reverse=True
    )[:5]

    # Combine both lists without duplicates
    combined = {}
    
    for process in top_cpu + top_memory:
        combined[process["pid"]] = process

    return list(combined.values())

def get_drives():
    """Get information about all accessible drives."""

    drives = []

    for partition in psutil.disk_partitions():

        # Ignore CD/DVD drives
        if "cdrom" in partition.opts.lower():
            continue

        try:
            usage = psutil.disk_usage(partition.mountpoint)

            drives.append({
                "letter": partition.device,
                "total_gb": round(
                    usage.total / (1024 ** 3), 2
                ),
                "used_gb": round(
                    usage.used / (1024 ** 3), 2
                ),
                "free_gb": round(
                    usage.free / (1024 ** 3), 2
                ),
                "usage_percent": usage.percent
            })

        except (PermissionError, OSError):
            continue

    return drives


def get_uptime():
    """Calculate system uptime."""

    boot_time = psutil.boot_time()
    current_time = datetime.now().timestamp()

    uptime_seconds = int(current_time - boot_time)

    days = uptime_seconds // 86400
    hours = (uptime_seconds % 86400) // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds
    }


def get_system_info():

    # CPU
    cpu_usage = psutil.cpu_percent(interval=1)

    cpu_frequency = psutil.cpu_freq()

    # RAM
    memory = psutil.virtual_memory()

    # Main C drive
    disk = psutil.disk_usage("C:\\")

    # Battery
    battery = psutil.sensors_battery()

    if battery:
        battery_data = {
            "percentage": battery.percent,
            "plugged_in": battery.power_plugged
        }
    else:
        battery_data = {
            "percentage": None,
            "plugged_in": None
        }

    # Network
    network = psutil.net_io_counters()

    # Temperature
    try:
        temperatures = psutil.sensors_temperatures()
    except Exception:
        temperatures = {}

    return {

        "timestamp": datetime.now().isoformat(),

        "system": {
            "os": platform.system(),
            "os_version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        },

        "cpu": {
            "usage_percent": cpu_usage,
            "cores": psutil.cpu_count(logical=False),
            "logical_processors": psutil.cpu_count(logical=True),
            "frequency_mhz": round(
                cpu_frequency.current, 2
            ) if cpu_frequency else None
        },

        "memory": {
            "total_gb": round(
                memory.total / (1024 ** 3), 2
            ),
            "used_gb": round(
                memory.used / (1024 ** 3), 2
            ),
            "available_gb": round(
                memory.available / (1024 ** 3), 2
            ),
            "usage_percent": memory.percent
        },

        "disk": {
            "total_gb": round(
                disk.total / (1024 ** 3), 2
            ),
            "used_gb": round(
                disk.used / (1024 ** 3), 2
            ),
            "free_gb": round(
                disk.free / (1024 ** 3), 2
            ),
            "usage_percent": disk.percent
        },

        "battery": battery_data,

        "network": {
            "bytes_sent": network.bytes_sent,
            "bytes_received": network.bytes_recv
        },

        "processes": get_processes(),

        "drives": get_drives(),

        "uptime": get_uptime(),

        "temperature": temperatures
    }


if __name__ == "__main__":

    from pprint import pprint

    data = get_system_info()

    pprint(data)