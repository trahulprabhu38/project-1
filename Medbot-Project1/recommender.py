import random

tips = {
    "POSITIVE": [
        "Keep journaling your positive thoughts!",
        "Take a mindful walk today.",
    ],
    "NEGATIVE": [
        "Try a 5-minute breathing exercise.",
        "Talk to a friend you trust.",
    ],
    "NEUTRAL": [
        "Practice gratitude journaling.",
        "Try doing light stretches for 10 minutes.",
    ]
}

def get_recommendation(sentiment):
    return random.choice(tips.get(sentiment, tips["NEUTRAL"]))
