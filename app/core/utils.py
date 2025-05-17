import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union


def generate_order_number() -> str:
    now = datetime.now()
    date_part = f"ORD-{now.year % 100:02d}{now.month:02d}{now.day:02d}"
    random_part = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

    return f"{date_part}-{random_part}"


def date_range(
    start_date: datetime, end_date: datetime, interval: str = "day"
) -> List[datetime]:
    dates = []
    current_date = start_date

    if interval == "day":
        delta = timedelta(days=1)
    elif interval == "week":
        delta = timedelta(weeks=1)
    elif interval == "month":
        delta = timedelta(days=30)
    elif interval == "year":
        delta = timedelta(days=365)
    else:
        delta = timedelta(days=1)

    while current_date <= end_date:
        dates.append(current_date)
        current_date += delta

    return dates


def format_money(amount: float) -> str:
    return f"${amount:.2f}"


def calculate_percentage_change(old_value: float, new_value: float) -> float:
    if old_value == 0:
        return float("inf") if new_value > 0 else 0

    return ((new_value - old_value) / old_value) * 100
