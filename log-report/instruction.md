An Apache-style access log is available at `/app/access.log`. Create `/app/report.json` as a JSON summary of that log.

The output must satisfy these success criteria:

1. `/app/report.json` exists and is valid JSON.
2. The JSON value is an object with exactly these keys: `total_requests`, `unique_ips`, and `top_path`.
3. `total_requests` is the number of non-empty lines in `/app/access.log`.
4. `unique_ips` is the number of distinct client IP addresses. The client IP is the first whitespace-separated field on each non-empty log line.
5. `top_path` is the requested URL path with the highest request count. The path is the URL path inside the quoted HTTP request, such as `/index.html` in `GET /index.html HTTP/1.1`. If multiple paths have the same highest count, use the one that appears earliest in the log.
