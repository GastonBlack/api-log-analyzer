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