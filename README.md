# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.
The game is a number-guessing game built with Streamlit. It picks a secret number in a range set by the difficulty (Easy, Normal or Hard). You guess it in a limited number of attempts, and after each guess a hint tells you to go higher or lower. A correct guess wins, running out of attempts loses, and fewer attempts earn a higher score.

- [X] Detail which bugs you found.
1. The message hints says the opposite of what it should.
2. The secret turns into text on every other guess
3. When you press the new gam button, a new game doesn't full reset
4. Diffculty and range don't match
5. The attemp count if off by one
6. Invalid input uses up an attempt
7. Scoring is inconsistent
8. Input ins't validated
9. The logic isn't wired up. Every function in logic_utils.py raises NotImplementedError, so the tests in tests/ fail until the functions are moved over from app.py

- [ ] Explain what fixes you applied.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the app with `python -m streamlit run app.py` and open http://localhost:8501. The sidebar shows the difficulty (Normal by default), the range (1 to 100) and the attempts allowed (8). The blue box says "Guess a number between 1 and 100. Attempts left: 8".
2. Open "Developer Debug Info" to see the secret number, for example 42. It stays the same no matter how many times you guess.
3. Type a guess that is too high, such as `80`, and press Enter or click "Submit Guess" once. The hint says "📉 Go LOWER!" and the blue box drops to "Attempts left: 7".
4. Guess too low, such as `20`. The hint says "📈 Go HIGHER!" and attempts left drops to 6. The input box clears after each guess.
5. Try invalid input: `abc`, `3.5` or `150`. Each shows an error ("Enter a whole number." or "Enter a number between 1 and 100.") and does not use up an attempt.
6. Guess the secret number. Balloons appear and the message reads "You won! The secret was 42. Final score: …". Any further guess shows "You already won. Start a new game to play again."
7. Click "New Game". The game resets with a new secret, 8 attempts and an empty guess history.
8. Switch the difficulty in the sidebar to Easy. A new game starts automatically, and the range and prompt both change to 1 to 20 with 6 attempts. (Hard is 1 to 200 with 5 attempts.)
9. Use up all your attempts without guessing correctly. On the last guess the message reads "Out of attempts! The secret was …", and the blue box shows "Attempts left: 0".

**Screenshot** *(optional)*: [Winning game showing balloons and the game summary table]
assets/screenshot.gif

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
#platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\cvabw\OneDrive\_Codepath\AI 110\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.15.1
collected 29 items                                                                     

tests\test_edge_cases.py .......................                                 [ 79%]
tests\test_game_logic.py ......                                                  [100%]

================================= 29 passed in 0.19s ==================================
```

## 🚀 Stretch Features

- [X] **Challenge 4: Enhanced UI.** The game now gives color-coded, hot/cold feedback and a summary of the session. The core game logic (`check_guess`, `parse_guess`, `update_score`) was not changed, and all tests still pass.

  **1. Hot/cold closeness: `get_temperature()` in `logic_utils.py` (new)**
  - Takes a guess, the secret and the current range, and returns a label and an emoji: `("Hot", "🔥")`, `("Warm", "🌡️")`, `("Cold", "🧊")` or `("Correct", "🎯")`.
  - Closeness is measured as a share of the range, so it is fair across difficulties: within 10% of the range is Hot, within 25% is Warm, anything further is Cold. Being 3 away is Hot on Normal (1 to 100) but only Warm on Easy (1 to 20).
  - It is a pure function with no Streamlit code, so it is covered by `test_temperature_scales_with_range` in `tests/test_game_logic.py`.

  **2. Color-coded hints: the submit handler in `app.py` (modified)**
  - The hint used to be a plain yellow `st.warning(message)`. It is now colored by closeness: 🔥 Hot shows as a red box (`st.error`), 🌡️ Warm as orange (`st.warning`) and 🧊 Cold as blue (`st.info`).
  - The direction from `check_guess` is kept, so a hint reads, for example, "🔥 **Hot!** 📉 Go LOWER!".
  - Turning off "Show hint" hides both the direction and the closeness.

  **3. Game summary: `render_summary()` in `app.py` (new, called from `render_status()`)**
  - After the first guess, a "Game summary" section appears with three `st.metric` cards: **Attempts used** (for example 3 / 8), **Score**, and **Result** (In progress, Won 🏆 or Lost 💀).
  - Below the cards, an `st.dataframe` table lists every guess this game, with the columns Guess #, Guess, Hint (Too High / Too Low / Win) and Closeness (🔥 Hot, 🧊 Cold, …).
  - Each guess is recorded in a new `st.session_state.log` list, which `start_new_game()` clears so the table starts fresh on New Game or a difficulty change.
  - When "Show hint" is off, the table shows only the guess number and guess, so it does not give the hints away.

  Example summary after winning in three guesses (secret 94):

  | Guess # | Guess | Hint | Closeness |
  |---|---|---|---|
  | 1 | 54 | Too Low | 🧊 Cold |
  | 2 | 97 | Too High | 🔥 Hot |
  | 3 | 94 | Win | 🎯 Correct |
