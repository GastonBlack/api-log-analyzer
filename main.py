from pathlib import Path
from colorama import init

from features import show_errors, show_status_codes, show_top_endpoints, show_total_lines, show_slow_requests
from helpers import load_lines

init(autoreset=True)
LOG_PATH = Path("sample_logs/api.log")


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
    print("5. Show slow requests")
    print("6. Exit")


# Calls menu
def main() -> None:
    lines = load_lines(LOG_PATH)

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
            show_slow_requests(lines)
        elif option == "6":
            print("Closing...")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()