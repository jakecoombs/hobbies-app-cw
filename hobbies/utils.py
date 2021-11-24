from datetime import date, datetime, timedelta


def calculate_pivot_date(age: int) -> datetime:
    today = date.today()
    days_per_year = 365.25
    return today - timedelta(days=(age*days_per_year))
