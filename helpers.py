def parse_log_line(line: str) -> dict:
    parts = line.split()

    return {
        "date": parts[0],
        "time": parts[1],
        "method": parts[2],
        "endpoint": parts[3],
        "status_code": int(parts[4]),
        "duration": parts[5],
    }