import csv
import subprocess
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

url = "http://127.0.0.1:8081/"
filename = datetime.now().strftime("k8s_crash_%Y%m%d_%H%M%S_%f.csv")
clock = time.perf_counter
origin = clock()

def probe(number):
    start = clock()
    try:
        with urllib.request.urlopen(url, timeout=0.5) as response:
            response.read()
            result = str(response.status)
    except OSError as error:
        result = type(error).__name__ + ": " + str(error)
    return number, start - origin, clock() - origin, result

with ThreadPoolExecutor(max_workers=12) as pool:
    baseline = [probe(i) for i in range(3)]
    if any(row[3] != "200" for row in baseline):
        raise SystemExit(f"Stopped before crash: baseline failed. {baseline}")

    jobs = []
    trigger = None
    first = clock()
    for i in range(120):
        time.sleep(max(0, first + i * 0.1 - clock()))
        if i == 20:
            trigger = clock() - origin
            command = pool.submit(subprocess.run,
                ["kubectl", "--context", "kind-sen421", "-n", "default", "exec", "deployment/web", "--", "nginx", "-s", "stop"],
                capture_output=True, text=True)
        jobs.append(pool.submit(probe, i + 3))

    rows = baseline + [job.result() for job in jobs]
    outcome = command.result()

with open(filename, "x", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["probe", "start_s", "finish_s", "result", "trigger_command_start_s"])
    writer.writerows([*row, trigger] for row in rows)

print("Saved:", filename)
print("Crash command exit code:", outcome.returncode)
if outcome.returncode:
    print(outcome.stderr.strip())
else:
    after = sorted((r for r in rows if r[1] >= trigger), key=lambda r: r[1])
    failed = [r for r in after if r[3] != "200"]
    print("Failed probes after trigger:", len(failed))
    if failed:
        recovered = next((r for r in after if r[1] > failed[0][1] and r[3] == "200"), None)
        if recovered:
            print("First failed probe start to next successful response:",
                  f"{recovered[2] - failed[0][1]:.3f} s")
        else:
            print("Recovery was not observed within the test window.")
    else:
        print("No failure was observed at this sampling interval.")

