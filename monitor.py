import subprocess
import time
import csv
from datetime import datetime

servers = ["8.8.8.8", "1.1.1.1", "10.255.255.1"]

failure_count = {}
total_checks = {}
successful_checks = {}
incident_id = 1
max_cycles = 5   # Number of monitoring cycles

print("Monitoring Started...\n")

for cycle in range(max_cycles):
    print(f"\n===== Cycle {cycle + 1} =====\n")

    for server in servers:

        total_checks[server] = total_checks.get(server, 0) + 1
        successful_checks.setdefault(server, 0)
        failure_count.setdefault(server, 0)

        response = subprocess.run(["ping", "-n", "1", server], stdout=subprocess.PIPE)

        if response.returncode == 0:
            print(f"{server} is UP")
            successful_checks[server] += 1
            failure_count[server] = 0

        else:
            failure_count[server] += 1

            if failure_count[server] == 1:
                severity = "WARNING"
            elif failure_count[server] == 2:
                severity = "CRITICAL"
            else:
                severity = "ESCALATED"

            print(f"{severity}: {server} is DOWN")

            with open("incident_log.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    f"INC{incident_id}",
                    datetime.now(),
                    server,
                    severity
                ])

            print(f"Incident INC{incident_id} logged.")
            incident_id += 1

            if severity == "ESCALATED":
                print(f"ESCALATION: {server} forwarded to Level 2 support")

    print("\n--- Status Summary ---")

    for server in servers:
        uptime = (successful_checks[server] / total_checks[server]) * 100
        print(f"{server} Uptime: {uptime:.2f}%")

    if cycle < max_cycles - 1:
        print("\nWaiting 5 seconds before next cycle...\n")
        time.sleep(5)

print("\nMonitoring Completed Successfully.")