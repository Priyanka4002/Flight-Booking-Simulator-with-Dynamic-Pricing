# utils.py
import random, string
from datetime import datetime

def generate_pnr(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits
    return "PNR" + "".join(random.choice(chars) for _ in range(length))

def flight_duration_minutes(departure, arrival):
    if departure and arrival:
        return int((arrival - departure).total_seconds() // 60)
    return 0

def random_name():
    first = ["Ananya", "Ravi", "Neha", "Arjun", "Priya", "Kiran", "Meena", "Dev", "Asha", "Sanjay"]
    last = ["Patel", "Sharma", "Rao", "Kumar", "Reddy", "Nair", "Das", "Iyer"]
    return f"{random.choice(first)} {random.choice(last)}"