import json
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
REQUEST_RE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH|OPTIONS) (\S+) ')

paths = Counter()
ips = set()
total = 0
first_seen_path_index = {}

with LOG_PATH.open("r", encoding="utf-8") as log_file:
    for line in log_file:
        line = line.strip()
        if not line:
            continue

        total += 1
        parts = line.split()
        ips.add(parts[0])

        match = REQUEST_RE.search(line)
        if match:
            path = match.group(1)
            paths[path] += 1
            first_seen_path_index.setdefault(path, total)

if not paths:
    raise RuntimeError("no request paths found in access log")

top_path = max(paths, key=lambda path: (paths[path], -first_seen_path_index[path]))

report = {
    "total_requests": total,
    "unique_ips": len(ips),
    "top_path": top_path,
}

with REPORT_PATH.open("w", encoding="utf-8") as report_file:
    json.dump(report, report_file, sort_keys=True)
    report_file.write("\n")

print(f"wrote {REPORT_PATH}")
