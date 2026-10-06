import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    get_temperature,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header(":material/tune: Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.markdown(
    f":material/straighten: Range: **{low} to {high}**  \n"
    f":material/target: Attempts allowed: **{attempt_limit}**"
)

def start_new_game():
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.log = []
    st.session_state.difficulty = difficulty


if "score" not in st.session_state:
    st.session_state.score = 0

# A secret picked for another difficulty may be outside this range
if st.session_state.get("difficulty") != difficulty:
    start_new_game()

st.subheader("Make a guess")

# Reserve these spots now but fill them in last, after a submitted guess
# has been counted; otherwise they show the count from before the guess.
info_box = st.empty()
debug_box = st.expander("Developer Debug Info", icon=":material/bug_report:").empty()


def render_status():
    info_box.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}"
    )
    with debug_box.container():
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

    render_summary()


def render_summary():
    """Show the score row and a table of every guess made this game."""
    log = st.session_state.log
    if not log:
        return

    st.subheader("Game summary")
    result = {"playing": "In progress", "won": "Won 🏆", "lost": "Lost 💀"}
    with st.container(horizontal=True):
        st.metric("Attempts used", f"{st.session_state.attempts} / {attempt_limit}", border=True)
        st.metric("Score", st.session_state.score, border=True)
        st.metric("Result", result[st.session_state.status], border=True)

    # The hint columns would give the answer away when hints are off
    columns = ["Guess #", "Guess", "Hint", "Closeness"] if show_hint else ["Guess #", "Guess"]
    st.dataframe([{c: row[c] for c in columns} for row in log], hide_index=True)


# A form sends the typed guess and the click in one rerun; with a separate
# text box and button, the first click often only commits the text.
with st.form("guess_form", clear_on_submit=True):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button(
        "Submit Guess", type="primary", icon=":material/send:", width="stretch"
    )

with st.container(horizontal=True, vertical_alignment="center"):
    new_game = st.button("New Game", icon=":material/refresh:")
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game()
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_status()
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)
        temp, temp_emoji = get_temperature(guess_int, st.session_state.secret, low, high)

        st.session_state.log.append({
            "Guess #": st.session_state.attempts,
            "Guess": guess_int,
            "Hint": outcome,
            "Closeness": f"{temp_emoji} {temp}",
        })

        # Color the hint by how close the guess was: red hot, orange warm, blue cold
        if show_hint and outcome != "Win":
            hint_box = {"Hot": st.error, "Warm": st.warning, "Cold": st.info}[temp]
            hint_box(f"{temp_emoji} **{temp}!** {message}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

render_status()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
