import pytest

from logic_utils import parse_guess


# --- Inputs that should already work ---

@pytest.mark.parametrize("raw, expected", [
    ("1", 1),
    ("50", 50),
    ("100", 100),
    (" 42 ", 42),  # surrounding whitespace is harmless
])
def test_valid_guesses_are_accepted(raw, expected):
    ok, value, err = parse_guess(raw, 1, 100)
    assert ok is True
    assert value == expected
    assert err is None


@pytest.mark.parametrize("raw", [None, "", "   ", "abc", "1,000", "nan", "inf", "1e400"])
def test_non_numbers_are_rejected_without_crashing(raw):
    ok, value, err = parse_guess(raw, 1, 100)
    assert ok is False
    assert value is None
    assert err  # player gets a message, not a stack trace


# --- Edge case 1: negative numbers and zero ---

@pytest.mark.parametrize("raw", ["-5", "-1", "0"])
def test_numbers_below_range_are_rejected(raw):
    # Secret is never below 1, so these guesses can't be meaningful
    ok, value, err = parse_guess(raw, 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in err


# --- Edge case 2: decimals ---

@pytest.mark.parametrize("raw", ["3.9", "-0.5", "50.5"])
def test_decimals_are_rejected(raw):
    # Bug: "3.9" was silently truncated to 3, so it could count as a win on secret 3
    ok, value, err = parse_guess(raw, 1, 100)
    assert ok is False
    assert value is None
    assert err


# --- Edge case 3: extremely large values ---

@pytest.mark.parametrize("raw", ["101", "500", "99999999999999999999"])
def test_numbers_above_range_are_rejected(raw):
    ok, value, err = parse_guess(raw, 1, 100)
    assert ok is False
    assert value is None
    assert "between 1 and 100" in err


# --- Range follows difficulty ---

def test_range_boundaries_are_inclusive():
    assert parse_guess("1", 1, 20)[0] is True
    assert parse_guess("20", 1, 20)[0] is True
    assert parse_guess("21", 1, 20)[0] is False


def test_range_message_reflects_difficulty():
    # Easy is 1-20, so 50 is out of range there even though it's fine on Normal
    ok, _, err = parse_guess("50", 1, 20)
    assert ok is False
    assert "between 1 and 20" in err
