import json
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
REQUEST_RE = re.compile(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH|OPTIONS) (\S+) ')


def read_report():
    with REPORT_PATH.open("r", encoding="utf-8") as report_file:
        return json.load(report_file)


def expected_values():
    total_requests = 0
    unique_ips = set()
    path_counts = Counter()
    first_seen = {}

    with LOG_PATH.open("r", encoding="utf-8") as log_file:
        for line in log_file:
            line = line.strip()
            if not line:
                continue

            total_requests += 1
            fields = line.split()
            unique_ips.add(fields[0])

            request_match = REQUEST_RE.search(line)
            if request_match is None:
                continue
            path = request_match.group(1)
            path_counts[path] += 1
            first_seen.setdefault(path, total_requests)

    assert path_counts, "access log must contain at least one parseable request path"
    top_path = max(path_counts, key=lambda path: (path_counts[path], -first_seen[path]))

    return {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "top_path": top_path,
    }


def test_criterion_1_report_exists_and_is_valid_json():
    """Verifies success criterion 1: /app/report.json exists and is valid JSON."""
    assert REPORT_PATH.exists(), "/app/report.json does not exist"
    read_report()


def test_criterion_2_report_has_exact_schema():
    """Verifies success criterion 2: the JSON object has exactly the required keys and types."""
    report = read_report()
    assert isinstance(report, dict), "report must be a JSON object"
    assert set(report) == {"total_requests", "unique_ips", "top_path"}
    assert isinstance(report["total_requests"], int), "total_requests must be an integer"
    assert isinstance(report["unique_ips"], int), "unique_ips must be an integer"
    assert isinstance(report["top_path"], str), "top_path must be a string"


def test_criterion_3_total_requests_matches_non_empty_log_lines():
    """Verifies success criterion 3: total_requests equals the non-empty line count."""
    report = read_report()
    expected = expected_values()
    assert report["total_requests"] == expected["total_requests"]


def test_criterion_4_unique_ips_matches_distinct_client_addresses():
    """Verifies success criterion 4: unique_ips equals the number of distinct first-field IPs."""
    report = read_report()
    expected = expected_values()
    assert report["unique_ips"] == expected["unique_ips"]


def test_criterion_5_top_path_matches_most_frequent_path_with_tie_break():
    """Verifies success criterion 5: top_path is the most frequent path, first-seen wins ties."""
    report = read_report()
    expected = expected_values()
    assert report["top_path"] == expected["top_path"]
