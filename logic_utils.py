def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw.strip())
    except ValueError:
        return False, None, "Enter a whole number."

    if not low <= value <= high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def get_temperature(guess, secret, low, high):
    """
    Describe how close a guess is, scaled to the difficulty's range.

    Returns: (label, emoji), one of "Correct", "Hot", "Warm" or "Cold"
    """
    if guess == secret:
        return "Correct", "🎯"

    closeness = abs(guess - secret) / (high - low)
    if closeness <= 0.10:
        return "Hot", "🔥"
    if closeness <= 0.25:
        return "Warm", "🌡️"
    return "Cold", "🧊"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
