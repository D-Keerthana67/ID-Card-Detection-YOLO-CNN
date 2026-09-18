import csv
from datetime import datetime
from pathlib import Path


class ViolationManager:
    def __init__(self, warning_limit, fine_amount, log_path):
        self.warning_limit = warning_limit
        self.fine_amount = fine_amount
        self.log_path = Path(log_path)
        self.warning_counts = {}
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def register_violation(self, student_id):
        count = self.warning_counts.get(student_id, 0)
        if count < self.warning_limit:
            count += 1
            self.warning_counts[student_id] = count
            return "warning", count
        self._record_fine(student_id)
        return "fine", self.fine_amount

    def _record_fine(self, student_id):
        exists = self.log_path.exists()
        with self.log_path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not exists:
                writer.writerow(["timestamp", "student_id", "fine_amount"])
            writer.writerow([datetime.now().isoformat(timespec="seconds"), student_id, self.fine_amount])
