import random
from datetime import datetime

def calculate_dynamic_price(base_fare, seats_available, capacity, departure_time):
    seat_factor = (1 - (seats_available / capacity)) * 0.4
    hours_left = max((departure_time - datetime.now()).total_seconds() / 3600, 0)

    if hours_left < 24:
        time_factor = 0.5
    elif hours_left < 72:
        time_factor = 0.3
    else:
        time_factor = 0.1

    demand_factor = random.uniform(-0.05, 0.25)
    multiplier = 1 + seat_factor + time_factor + demand_factor
    return round(base_fare * multiplier, 2)
