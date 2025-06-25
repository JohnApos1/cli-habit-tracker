from datetime import datetime, date
from utils import *

DATA_FILE = "data.json"

def add_habit(name):
    data = load_data()
    if name in data:
        print(f"Habit '{name}' already exists.")
    else:
        category = input("Enter category (e.g. Health, Focus, Self-Care): ")
        data[name] = {
            "category": category,
            "log": {}
        }
        print(f"Habit '{name}' added under category '{category}'.")
    save_data(data=data)

def mark_habit(name, custom_date=None):
    data = load_data()
    today = str(custom_date or date.today())
    if name not in data:
        print(f"Habit '{name}' not found. Add it first.")
        return
    data[name]["log"][today] = True
    print(f"Habit '{name}' marked as done for {today}.")
    save_data(data=data)

def show_habits():
    data = load_data()
    if not data:
        print("No habits found.")
        return
    print("\n📈 Habit Progress:\n")
    for habit, entry in data.items():
        log = entry.get("log", {})
        print(draw_habit_graph(habit, log))
    print("")

def delete_habit(name):
    data = load_data()
    if name in data:
        del data[name]
        save_data(data=data)
        print(f"Habit '{name}' deleted.")
    else:
        print("Habit not found.")

def reset_habit(name):
    data = load_data()
    if name in data:
        data[name]["log"] = {}
        save_data(data=data)
        print(f"Habit '{name}' has been reset.")
    else:
        print("Habit not found.")

def menu():
    data = load_data()
    check_today_reminders(data)

    while True:
        print("\n=== CLI Habit Tracker ===")
        print("1. Add Habit")
        print("2. Mark Habit as Done")
        print("3. Show Habit Progress")
        print("4. Delete Habit")
        print("5. Reset Habit")
        print("6. Dashboard")
        print("7. Export to CSV")
        print("8. Load Backup")
        print("9. View Calendar")
        print("10. Show Bar Graphs")
        print("11. Start Habit Timer")
        print("12. Exit")

        choice = input("Choose an option (1–12): ")

        if choice == "1":
            name = input("Enter habit name: ")
            add_habit(name)

        elif choice == "2":
            name = input("Enter habit name: ")
            date_input = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            try:
                custom_date = datetime.strptime(date_input, "%Y-%m-%d").date() if date_input else None
                mark_habit(name, custom_date)
            except ValueError:
                print("Invalid date format.")

        elif choice == "3":
            show_habits()

        elif choice == "4":
            name = input("Enter habit name to delete: ")
            delete_habit(name)

        elif choice == "5":
            name = input("Enter habit name to reset: ")
            reset_habit(name)

        elif choice == "6":
            data = load_data()
            generate_dashboard(data)

        elif choice == "7":
            data = load_data()
            export_to_csv(data)

        elif choice == "8":
            backups = list_backups()
            if not backups:
                print("No backups found.")
            else:
                print("Available backups:")
                for i, b in enumerate(backups):
                    print(f"{i + 1}. {b}")
                try:
                    index = int(input("Select backup to load: ")) - 1
                    if 0 <= index < len(backups):
                        load_backup(backups[index])
                except:
                    print("Invalid selection.")

        elif choice == "9":
            data = load_data()
            name = input("Enter habit name: ")
            if name in data:
                show_calendar(name, data[name].get("log", {}))
            else:
                print("Habit not found.")

        elif choice == "10":
            data = load_data()
            view = input("View type (weekly/monthly/all): ").strip().lower()
            show_bar_progress(data, view)

        elif choice == "11":
            name = input("Enter habit name to time: ")
            try:
                mins = int(input("Enter duration in minutes: "))
                start_habit_timer(name, mins)
            except ValueError:
                print("Invalid number.")

        elif choice == "12":
            data = load_data()
            auto_backup(data)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
