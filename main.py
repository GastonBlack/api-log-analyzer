from pathlib import Path
from colorama import init, Fore, Style

init(autoreset=True)


LOG_PATH = Path("sample_logs/api.log")

######
####################
def load_lines() -> list[str]:
    content = LOG_PATH.read_text()
    return content.splitlines()


def show_total_lines(lines: list[str]) -> None:
    print(f"Total log lines: {len(lines)}")


def show_status_codes(lines: list[str]) -> None:
    stats = {"2": 0, "3": 0, "4": 0, "5": 0}

    for line in lines:
        parts = line.split()

        # Status code.
        code = parts[4][0]  # First char ["2xx", "3xx", "4xx", "5xx"].
        if code in stats:
            stats[code] += 1

    print(f"{Fore.GREEN}Good requests (2xx): {stats['2']}")
    print(f"{Fore.YELLOW}Redirections (3xx): {stats['3']}")
    print(f"{Fore.RED}Client errors (4xx): {stats['4']}")
    print(f"{Fore.RED}{Style.BRIGHT}Internal server errors (5xx): {stats['5']}")


def show_top_endpoints(lines: list[str]) -> None:
    endpoints = {}

    for line in lines:
        parts = line.split()

        method = parts[2]
        endpoint = parts[3]
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
        parts = line.split()

        method = parts[2]
        endpoint = parts[3]
        status_code = int(parts[4])
        duration = parts[5]

        if status_code >= 400:
            print(f"{status_code} {method} {endpoint} {duration}")



####################
######

# Menu
def show_menu() -> None:
    print("\n\n\n")
    print("########################")
    print("### API Log Analyzer ###")
    print("########################\n")
    print("1. Show total log lines")
    print("2. Show status codes")
    print("3. Show top endpoints")
    print("4. Show errors")
    print("5. Exit")


# Calls menu
def main() -> None:
    lines = load_lines()

    while True:
        show_menu()
        option = input("Choose an option: ")

        if option == "1":
            show_total_lines(lines)
        elif option == "2":
            show_status_codes(lines)
        elif option == "3":
            show_top_endpoints(lines)
        elif option == "4":
            show_errors(lines)
        elif option == "5":
            print("Closing...")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()