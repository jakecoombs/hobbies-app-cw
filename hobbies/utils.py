from datetime import date, timedelta


def calculate_pivot_date(age):
    today = date.today()
    days_per_year = 365.25
    return today - timedelta(days=(age*days_per_year))
