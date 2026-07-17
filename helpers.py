from pathlib import Path


def load_lines(log_path: Path) -> list[str]:
    content = log_path.read_text()
    return content.splitlines()


def parse_log_line(line: str) -> dict:
    parts = line.split()

    if len(parts) != 6:
        raise ValueError("Invalid log line format.")
    
    try:
        status_code = int(parts[4])
    except ValueError:
        raise ValueError("Invalid status code.")

    return {
        "date": parts[0],
        "time": parts[1],
        "method": parts[2],
        "endpoint": parts[3],
        "status_code": status_code,
        "duration": parts[5],
    }


def try_parse_log_line(line: str) -> dict | None:
    try:
        parsed_line = parse_log_line(line)
    except ValueError:
        return None 
    
    return parsed_line


def get_valid_log_entries(lines: list[str]) -> tuple[list[dict], int]:
    valid_entries = []
    invalid_count = 0

    for line in lines:
        parsed_line = try_parse_log_line(line)

        if parsed_line is None:
            invalid_count += 1
            continue

        valid_entries.append(parsed_line)
    
    return valid_entries, invalid_count