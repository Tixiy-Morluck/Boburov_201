import csv
import os

from config import TASKS_FILE, SESSIONS_FILE, REPORT_FILE, DATE_FMT
from models import Task


class TaskStorage:
    @staticmethod
    def load():
        tasks = []
        if not os.path.exists(TASKS_FILE):
            return tasks
        with open(TASKS_FILE, "r", encoding="utf-8", newline="") as f:
            r = csv.reader(f)
            next(r, None)
            for i, row in enumerate(r, 1):
                if len(row) >= 6:
                    tasks.append(Task.from_row(row, i))
        return tasks

    @staticmethod
    def save(tasks):
        with open(TASKS_FILE, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(Task.FIELDS)
            for t in tasks:
                w.writerow(t.to_row())


class SessionStorage:
    @staticmethod
    def log(session):
        new = not os.path.exists(SESSIONS_FILE)
        with open(SESSIONS_FILE, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["login", "time_in", "time_out"])
            w.writerow([
                session.login,
                session.time_in.strftime(DATE_FMT),
                session.time_out.strftime(DATE_FMT) if session.time_out else "",
            ])


class ReportStorage:
    @staticmethod
    def write(session):
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("+------------------------------------+\n")
            f.write("| login | time_in | time_out |\n")
            f.write("|---------|------------|-------------|\n")
            f.write(
                f"|{session.login} | "
                f"{session.time_in.strftime(DATE_FMT)} | "
                f"{session.time_out.strftime(DATE_FMT)} |\n"
            )
            f.write("+------------------------------------+\n")