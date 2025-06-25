# CLI Habit Tracker 🧭

A powerful terminal-based habit tracker that lets you build better routines and stay consistent — with an interactive menu, backups, calendar view, Pomodoro timer, and more.

---

## ✨ Features

- ✅ **Interactive Menu** – No command memorization needed
- 📅 **Calendar View** – View habit completion over the full month
- 🔄 **Auto Backup & Load** – Automatically saves backups and lets you restore any version
- 🗂️ **Habit Categories** – Organize habits by type (e.g. Health, Focus, etc.)
- 📊 **Bar Graph Progress** – Visualize your week/month performance
- 🎯 **Daily Reminders** – Get notified if you forget to mark your habits
- ⏱️ **Pomodoro Timer** – Focus timer with time tracking per habit
- 📂 **CSV Export** – Export all logs for analysis
- 🧮 **Streak Tracking** – See current and longest streaks

---

## 🖥️ How to Use

1. **Install dependencies**:
```bash
pip install plyer
```

2. **Run the tracker**:
```bash
python tracker.py
```

3. **Choose from the menu**:
```
1. Add Habit
2. Mark Habit as Done
3. Show Habit Progress
...
12. Exit
```

---

## 📦 Installation (Optional Build)
You can build a standalone executable with:
```bash
pip install pyinstaller
pyinstaller --onefile tracker.py
```
The final `.exe` will be in the `/dist` folder.

---

## 📁 Folder Structure
```
cli-habit-tracker/
├── tracker.py         # Main app logic
├── utils.py           # All helper logic (graphs, backups, timer, etc.)
├── data.json          # Your saved habits
├── backups/           # Auto-saved JSON backups
├── habit_export.csv   # Optional CSV export
```

---

## 🤝 Contributions
Pull requests welcome! You can fork the repo and submit your upgrades, like:
- Web dashboard
- Color themes
- Sound alerts
- Tag filters

---

## 📜 License
MIT – use it, remix it, share it freely.

---
Built with ☕ and focus by [JohnApos1].
