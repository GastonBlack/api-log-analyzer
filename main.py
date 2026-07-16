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
    print("3. Exit")


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
            print("Closing...")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()