import json
import os
import csv
import time
import shutil
import calendar
from datetime import date, timedelta, datetime
from plyer import notification

DATA_FILE = "data.json"

# === CORE FUNCTIONS ===

def load_data(filename=DATA_FILE):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(filename=DATA_FILE, data=None):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# === HABIT DISPLAY ===

def calculate_streaks(record):
    today = date.today()
    days = sorted(record.keys())
    days = [date.fromisoformat(d) for d in days if record[d]]
    if not days:
        return 0, 0

    longest = 0
    streak = 0

    for i in range(len(days)):
        if i == 0 or (days[i] - days[i - 1]).days == 1:
            streak += 1
        else:
            streak = 1
        longest = max(longest, streak)

    streak = 0
    for i in range(0, 100):
        day = today - timedelta(days=i)
        if record.get(day.isoformat()):
            streak += 1
        else:
            break

    return streak, longest

def draw_habit_graph(habit_name, record):
    today = date.today()
    past_week = [(today - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    bar = ''.join("▓" if record.get(day) else "░" for day in past_week)
    count = sum(1 for day in past_week if record.get(day))

    current_streak, longest_streak = calculate_streaks(record)

    output = f"\n╭─ {habit_name.upper()} ──────────────────────────╮\n"
    output += f"│ Progress : {bar} ({count}/7)\n"
    output += f"│ Streak   : 🔥 {current_streak} current | 🏆 {longest_streak} longest\n"
    output += "╰────────────────────────────────────────╯\n"
    return output

# === ADDITIONAL FEATURES ===

def show_bar_progress(data, view="weekly"):
    print("\n📊 HABIT PROGRESS BARS\n─────────────────────────────")
    today = date.today()

    for habit, entry in data.items():
        log = entry.get("log", {})
        count = 0
        if view == "weekly":
            week_ago = today - timedelta(days=6)
            for d, done in log.items():
                if date.fromisoformat(d) >= week_ago and done:
                    count += 1
            max_count = 7
        elif view == "monthly":
            month_start = today.replace(day=1)
            for d, done in log.items():
                if date.fromisoformat(d) >= month_start and done:
                    count += 1
            max_count = calendar.monthrange(today.year, today.month)[1]
        else:
            count = sum(1 for done in log.values() if done)
            max_count = 30 if count < 30 else count

        bar_length = 20
        filled = int((count / max_count) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)

        print(f"{habit:15} | {bar} | {count}/{max_count}")

def show_calendar(habit_name, record):
    today = date.today()
    year = today.year
    month = today.month
    print(f"\n📅 {habit_name.upper()} - {calendar.month_name[month]} {year}")
    print("Su Mo Tu We Th Fr Sa")
    cal = calendar.monthcalendar(year, month)
    for week in cal:
        line = ""
        for day in week:
            if day == 0:
                line += "   "
            else:
                day_str = date(year, month, day).isoformat()
                mark = "▓" if record.get(day_str) else "░"
                line += f"{mark} "
        print(line)

def export_to_csv(data, filename="habit_export.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Habit", "Date", "Completed"])
        for habit, entry in data.items():
            for date_str, done in entry.get("log", {}).items():
                writer.writerow([habit, date_str, "Yes" if done else "No"])
    print(f"✅ Exported to {filename}")

def auto_backup(data, folder="backups"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(folder, f"backup-{timestamp}.json")
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"🔄 Backup saved as {filename}")

def list_backups(folder="backups"):
    try:
        files = sorted(os.listdir(folder))
        return [f for f in files if f.endswith(".json")]
    except FileNotFoundError:
        return []

def load_backup(filename, folder="backups", destination=DATA_FILE):
    full_path = os.path.join(folder, filename)
    if not os.path.exists(full_path):
        print("❌ Backup file not found.")
        return
    shutil.copyfile(full_path, destination)
    print(f"✅ Restored backup from {filename}")

def generate_dashboard(data):
    total_habits = len(data)
    total_marks = sum(1 for entry in data.values() for v in entry.get("log", {}).values() if v)
    top_streak = 0
    top_habit = None
    for name, entry in data.items():
        current, longest = calculate_streaks(entry.get("log", {}))
        if longest > top_streak:
            top_streak = longest
            top_habit = name
    print("\n📊 DASHBOARD\n─────────────")
    print(f"📁 Total Habits  : {total_habits}")
    print(f"✅ Total Marks   : {total_marks}")
    if top_habit:
        print(f"🏆 Top Streak    : {top_streak} days by '{top_habit}'")
    print("")

def check_today_reminders(data):
    today = date.today().isoformat()
    unmarked = []
    for habit, entry in data.items():
        log = entry.get("log", {})
        if today not in log or not log.get(today):
            unmarked.append(habit)
    if unmarked:
        message = f"You haven't marked: {', '.join(unmarked)}"
        try:
            notification.notify(
                title="⏰ Daily Habit Reminder",
                message=message,
                timeout=5
            )
        except Exception as e:
            print("🔕 Notification failed:", e)

def start_habit_timer(name, duration=25):
    print(f"\n⏱️ Starting timer for '{name}' ({duration} min)... Press Ctrl+C to stop early.\n")
    try:
        for i in range(duration, 0, -1):
            print(f"⏳ {i} min left...", end="\r")
            time.sleep(60)  # use time.sleep(1) for testing
    except KeyboardInterrupt:
        print("\n⛔ Timer interrupted.")
    print(f"✅ Timer complete for '{name}'!")
    data = load_data(DATA_FILE)
    if name not in data:
        print("Habit not found.")
        return
    data[name]["minutes"] = data[name].get("minutes", 0) + duration
    save_data(DATA_FILE, data)
    print(f"🧮 Total time on '{name}': {data[name]['minutes']} min")
