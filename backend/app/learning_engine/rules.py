MASTERY_WEAK_THRESHOLD = 50
MASTERY_READY_THRESHOLD = 70
MASTERY_STRONG_THRESHOLD = 85


def classify_mastery(mastery: float) -> str:
    if mastery < MASTERY_WEAK_THRESHOLD:
        return "weak"
    if mastery < MASTERY_READY_THRESHOLD:
        return "practicing"
    if mastery < MASTERY_STRONG_THRESHOLD:
        return "ready"
    return "strong"
