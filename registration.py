from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple, Dict

# --- Model data sederhana ---
@dataclass
class RegistrationData:
    student_id: str
    selected_courses: List[str]
    courses_taken: List[str]
    total_sks: int
    course_prerequisites: Dict[str, List[str]]
    course_schedule: Dict[str, List[Tuple[str, str]]]


# --- Abstraksi Validation Rule (DIP/OCP) ---
class IValidationRule(ABC):
    @abstractmethod
    def validate(self, data: RegistrationData) -> Tuple[bool, str]:
        """Return (is_valid, message)."""
        pass

# --- Implementasi konkrit ---
class SksLimitRule(IValidationRule):
    def __init__(self, max_sks: int):
        self.max_sks = max_sks

    def validate(self, data: RegistrationData) -> Tuple[bool, str]:
        if data.total_sks > self.max_sks:
            return False, f"Total SKS ({data.total_sks}) melebihi batas maksimum ({self.max_sks})."
        return True, "SKS dalam batas."

class PrerequisiteRule(IValidationRule):
    def validate(self, data: RegistrationData) -> Tuple[bool, str]:
        missing = []
        for course in data.selected_courses:
            reqs = data.course_prerequisites.get(course, [])
            for r in reqs:
                if r not in data.courses_taken:
                    missing.append((course, r))

        if missing:
            msgs = [f"{c} butuh prasyarat {r}" for c, r in missing]
            return False, "; ".join(msgs)

        return True, "Semua prasyarat terpenuhi."

class JadwalBentrokRule(IValidationRule):
    """Rule untuk mendeteksi bentrok jadwal antar mata kuliah."""

    def _overlap(self, range1: str, range2: str) -> bool:
        def to_minutes(t: str) -> int:
            h, m = map(int, t.split(':'))
            return h * 60 + m

        s1, e1 = range1.split('-')
        s2, e2 = range2.split('-')
        return not (to_minutes(e1) <= to_minutes(s2) or to_minutes(e2) <= to_minutes(s1))

    def validate(self, data: RegistrationData) -> Tuple[bool, str]:
        schedule_items = []

        for course in data.selected_courses:
            times = data.course_schedule.get(course, [])
            for day, rng in times:
                schedule_items.append((course, day, rng))

        conflicts = []
        n = len(schedule_items)

        for i in range(n):
            c1, d1, r1 = schedule_items[i]
            for j in range(i + 1, n):
                c2, d2, r2 = schedule_items[j]
                if d1 == d2 and self._overlap(r1, r2) and c1 != c2:
                    conflicts.append((c1, c2, d1, r1, r2))

        if conflicts:
            msgs = [
                f"{a} bentrok dengan {b} pada {day} ({r1} vs {r2})"
                for a, b, day, r1, r2 in conflicts
            ]
            return False, "; ".join(msgs)

        return True, "Tidak ada bentrok jadwal."

# --- Koordinator (SRP) ---
class RegistrationService:
    def __init__(self, rules: List[IValidationRule]):
        self.rules = rules  # Dependency Injection

    def validate(self, data: RegistrationData) -> Tuple[bool, List[str]]:
        is_all_ok = True
        messages = []

        for rule in self.rules:
            ok, msg = rule.validate(data)
            messages.append(f"{rule.__class__.__name__}: {msg}")
            if not ok:
                is_all_ok = False

        return is_all_ok, messages

# --- Contoh penggunaan (untuk challenge OCP) ---
if __name__ == "__main__":

    course_prereqs = {
        "MATH201": ["MATH101"],
        "CS301": ["CS201"],
    }

    course_schedule = {
        "MATH201": [("Mon", "08:00-10:00")],
        "CS301": [("Mon", "09:00-11:00")],  # Bentrok
        "ENG101": [("Tue", "10:00-12:00")],
    }

    data = RegistrationData(
        student_id="A001",
        selected_courses=["MATH201", "CS301"],
        courses_taken=["MATH101"],
        total_sks=8,
        course_prerequisites=course_prereqs,
        course_schedule=course_schedule,
    )

    rules = [
        SksLimitRule(max_sks=24),
        PrerequisiteRule(),
        JadwalBentrokRule(),  # Challenge OCP → ditambah tanpa ubah service
    ]

    service = RegistrationService(rules)
    ok, msgs = service.validate(data)

    print("Hasil Validasi:")
    for m in msgs:
        print(" -", m)

    print("\nStatus Akhir:", "VALID" if ok else "TIDAK VALID")
