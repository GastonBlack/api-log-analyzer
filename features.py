from colorama import Fore, Style
from helpers import get_valid_log_entries

SLOW_REQUEST_THRESHOLD_MS = 100 # > 100ms = slow request.

## Features

def show_total_lines(lines: list[str]) -> None:
    valid_entries, invalid_count = get_valid_log_entries(lines)

    print(f"Total log lines: {len(lines)}")
    print(f"Valid log entries: {len(valid_entries)}")
    print(f"Invalid log entries: {invalid_count}")


def show_status_codes(lines: list[str]) -> None:
    stats = {"2": 0, "3": 0, "4": 0, "5": 0}
    valid_entries, invalid_count = get_valid_log_entries(lines)

    for parsed_line in valid_entries:

        code = str(parsed_line["status_code"])[0]  # First char ["2xx", "3xx", "4xx", "5xx"].
        if code in stats:
            stats[code] += 1

    print(f"{Fore.GREEN}Good requests (2xx): {stats['2']}")
    print(f"{Fore.YELLOW}Redirections (3xx): {stats['3']}")
    print(f"{Fore.RED}Client errors (4xx): {stats['4']}")
    print(f"{Fore.RED}{Style.BRIGHT}Internal server errors (5xx): {stats['5']}")
    print(f"{Fore.LIGHTCYAN_EX}Skipped lines: {invalid_count}")


def show_top_endpoints(lines: list[str]) -> None:
    endpoints = {}
    valid_entries, invalid_count = get_valid_log_entries(lines)

    for parsed_line in valid_entries:

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
    print(f"{Fore.LIGHTCYAN_EX}Skipped lines: {invalid_count}")


def show_errors(lines: list[str]) -> None:
    print("Errors:")
    any_error = False
    valid_entries, invalid_count = get_valid_log_entries(lines)

    for parsed_line in valid_entries:
        method = parsed_line["method"]
        endpoint = parsed_line["endpoint"]
        status_code = parsed_line["status_code"]
        duration_ms = parsed_line["duration_ms"]

        if status_code >= 400:
            any_error = True
            print(f"{status_code} {method} {endpoint} {duration_ms}ms")

    if not any_error:
        print("No errors found.")
    else:
        print(f"{Fore.LIGHTCYAN_EX}Skipped lines: {invalid_count}")
    

def show_slow_requests(lines: list[str]) -> None:
    valid_entries, invalid_count = get_valid_log_entries(lines)
    any_slow_request = False

    print(f"Slow requests over {SLOW_REQUEST_THRESHOLD_MS}ms:")

    for parsed_line in valid_entries:
        if parsed_line["duration_ms"] > SLOW_REQUEST_THRESHOLD_MS:
            any_slow_request = True
            print(
                f"{parsed_line["status_code"]} {parsed_line["method"]} "
                f"{parsed_line["endpoint"]} lasted {Fore.LIGHTRED_EX}{parsed_line["duration_ms"]}{Fore.RESET} milliseconds."
            )

    if not any_slow_request:
        print("No slow requests found")
    
    print(f"{Fore.LIGHTCYAN_EX}Skipped lines: {invalid_count}")
