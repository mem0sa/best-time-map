DAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def calculate_daily_load(day, details):
    rating = details.get("rating", 0)
    reviews = details.get("reviews_count", 0)
    types = details.get("types", [])

    load = 0

    if day in ["Saturday", "Sunday"]:
        load += 30
    else:
        load += 10

    load += min(reviews / 100, 40)

    if rating >= 4.5:
        load += 20
    elif rating >= 4.0:
        load += 10

    if "restaurant" in types or "cafe" in types:
        load += 15
    if "bar" in types:
        load += 20
    if "bank" in types or "post_office" in types:
        load -= 10

    return load


def choose_time_range(day, details):
    if day in ["Saturday", "Sunday"]:
        return "11:00–13:00"

    if "restaurant" in details.get("types", []):
        return "14:00–16:00"

    return "10:00–12:00"


def get_visit_recommendation(details):
    weekly_recommendations = {}
    daily_loads = {}

    for day in DAY_NAMES:
        load = calculate_daily_load(day, details)
        daily_loads[day] = load
        weekly_recommendations[day] = choose_time_range(day, details)

    best_day = min(daily_loads, key=daily_loads.get)

    return {
        "weekly_recommendations": weekly_recommendations,
        "best_day": {
            "day": best_day,
            "time": weekly_recommendations[best_day]
        }
    }