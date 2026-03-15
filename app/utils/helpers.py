def calculate_budget_per_day(total_budget: float, days: int) -> float:
    return total_budget / days if days > 0 else 0

def format_city_name(city: str) -> str:
    return city.strip().title()
