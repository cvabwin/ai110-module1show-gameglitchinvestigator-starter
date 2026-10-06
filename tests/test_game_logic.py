from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_too_high_hint_says_go_lower():
    # Bug: "Too High" used to say "Go HIGHER!", sending the player the wrong way
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_hint_says_go_higher():
    # Bug: "Too Low" used to say "Go LOWER!", sending the player the wrong way
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_compares_numerically_not_as_text():
    # Bug: the secret was stringified on even attempts, so "9" > "10" alphabetically
    # made 9 vs 10 come back "Too High". Numbers must compare as numbers.
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low"
    outcome, _ = check_guess(100, 50)
    assert outcome == "Too High"
