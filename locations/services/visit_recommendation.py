DAY_NAMES = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

TYPE_WEIGHTS = {
    "restaurant": 0.9,
    "cafe": 0.8,
    "bar": 1.0,
    "shopping_mall": 0.95,
    "bank": 0.4,
    "post_office": 0.5,
}

W_REVIEWS = 0.35
W_RATING = 0.25
W_DAY = 0.25
W_TYPE = 0.15


def normalize_reviews(reviews):
    return min(reviews / 1000, 1)


def normalize_rating(rating):
    return rating / 5 if rating else 0.5


def day_factor(day):
    if day in ["Saturday", "Sunday"]:
        return 1.0
    if day == "Friday":
        return 0.7
    return 0.4


def type_factor(types):
    for t in types:
        if t in TYPE_WEIGHTS:
            return TYPE_WEIGHTS[t]
    return 0.6


def choose_time_range(day, types):
    if day in ["Saturday", "Sunday"]:
        return "11:00–13:00"
    if "restaurant" in types or "cafe" in types:
        return "14:00–16:00"
    return "10:00–12:00"


def calculate_load_score(day, details):
    reviews = details.get("reviews_count", 0)
    rating = details.get("rating", 0)
    types = details.get("types", [])

    score = (
        W_REVIEWS * normalize_reviews(reviews) +
        W_RATING * normalize_rating(rating) +
        W_DAY * day_factor(day) +
        W_TYPE * type_factor(types)
    )

    return round(score * 100, 1)


def get_visit_recommendation(details):
    weekly = {}
    loads = {}

    for day in DAY_NAMES:
        score = calculate_load_score(day, details)
        loads[day] = score
        weekly[day] = {
            "time": choose_time_range(day, details.get("types", [])),
            "load_score": score
        }

    best_day = min(loads, key=loads.get)

    return {
        "weekly_recommendations": weekly,
        "best_day": {
            "day": best_day,
            "time": weekly[best_day]["time"],
            "load_score": weekly[best_day]["load_score"],
            "reason": "Минимальный расчётный уровень загруженности",
        },
        "data_source": "calculated",
    }
