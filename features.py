from colorama import Fore, Style
from helpers import try_parse_log_line

## Features

def show_total_lines(lines: list[str]) -> None:
    print(f"Total log lines: {len(lines)}")


def show_status_codes(lines: list[str]) -> None:
    stats = {"2": 0, "3": 0, "4": 0, "5": 0}

    for line in lines:
        parsed_line = try_parse_log_line(line)

        if parsed_line is None:
            continue

        # Status code.
        code = str(parsed_line["status_code"])[0]  # First char ["2xx", "3xx", "4xx", "5xx"].
        if code in stats:
            stats[code] += 1

    print(f"{Fore.GREEN}Good requests (2xx): {stats['2']}")
    print(f"{Fore.YELLOW}Redirections (3xx): {stats['3']}")
    print(f"{Fore.RED}Client errors (4xx): {stats['4']}")
    print(f"{Fore.RED}{Style.BRIGHT}Internal server errors (5xx): {stats['5']}")


def show_top_endpoints(lines: list[str]) -> None:
    endpoints = {}

    for line in lines:
        parsed_line = try_parse_log_line(line)

        if parsed_line is None:
            continue

        method = parsed_line["method"]
        endpoint = parsed_line["endpoint"]

        key = f"{method} {endpoint}"

        if key not in endpoints:
            endpoints[key] = 0

        endpoints[key] += 1

    sorted_endpoints = sorted(
        endpoints.items(),
        key = lambda item: item[1],
        reverse=True
    )

    print("Top 10 endpoints:")

    for endpoint, count in sorted_endpoints[:10]:
        print(f"{endpoint}: {count}")


def show_errors(lines: list[str]) -> None:
    print("Errors:")

    for line in lines:
        parsed_line = try_parse_log_line(line)
        if parsed_line is None:
            continue

        method = parsed_line["method"]
        endpoint = parsed_line["endpoint"]
        status_code = parsed_line["status_code"]
        duration = parsed_line["duration"]

        if status_code >= 400:
            print(f"{status_code} {method} {endpoint} {duration}")