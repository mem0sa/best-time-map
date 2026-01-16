import random

DAY_NAMES = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]

HOURS = list(range(9, 22))

TYPE_WEIGHTS = {
    "restaurant": 0.9,
    "cafe": 0.8,
    "bar": 1.0,
    "shopping_mall": 0.95,
    "bank": 0.4,
    "post_office": 0.5,
}

DAY_FACTORS = {
    "Понедельник": 0.5,
    "Вторник": 0.5,
    "Среда": 0.5,
    "Четверг": 0.5,
    "Пятница": 0.7,
    "Суббота": 1,
    "Воскресенье": 0.9,
}

HOUR_FACTORS = {
    9: 0.25,
    10: 0.25,
    11: 0.35,
    12: 0.7,
    13: 0.8,
    14: 0.6,
    15: 0.45,
    16: 0.5,
    17: 0.7,
    18: 0.9,
    19: 1.0,
    20: 0.8,
    21: 0.7,
}

W_REVIEWS = 0.30
W_RATING = 0.20
W_DAY = 0.20
W_TYPE = 0.15
W_HOUR = 0.11
W_RANDOM = 0.04

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

def calculate_load_score(day, details, hour):
    reviews = details.get("reviews_count", 0)
    rating = details.get("rating", 0)
    types = details.get("types", [])

    score = (
        W_REVIEWS * normalize_reviews(reviews) +
        W_RATING * normalize_rating(rating) +
        W_DAY * DAY_FACTORS[day] +
        W_TYPE * type_factor(types) + 
        W_HOUR * HOUR_FACTORS[hour] + 
        W_RANDOM * random.random()
    )

    return round(score * 100, 1)


def get_visit_recommendation(details):
    table = {}
    best_time = {
        "day": None,
        "hour": None,
        "score": float("inf"),
    }
    worst_time = {"score": float("-inf")}
    best_time_on_weekends = {"score": float("inf")}
    
    for hour in HOURS:
        hour_label = f"{hour}:00"
        table[hour_label] = {}

        for day in DAY_NAMES:
            score = calculate_load_score(day, details, hour)

            table[hour_label][day] = score

            if score < best_time["score"]:
                best_time = {
                    "day": day,
                    "hour": hour,
                    "score": score,
                }
            if score < best_time_on_weekends["score"] and day in ["Суббота", "Воскресенье"]:
                best_time_on_weekends = {
                    "day": day,
                    "hour": hour,
                    "score": score
                }
            if score > worst_time["score"]:
                worst_time = {
                    "score": score
                }

    return {
        "table": table,
        "best_time": best_time,
        "worst_time": worst_time,
        'best_time_on_weekends': best_time_on_weekends
    }

