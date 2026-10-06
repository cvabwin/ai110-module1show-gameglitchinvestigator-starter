# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input    | Expected Behavior | Actual Behavior | Console Output / Error    | Suspected Code Location
|-------   |-------------------|-----------------|---------------------------|-------------------------
| 80       |  Go Lower         | Go Higher       | error in parsing "color:."| check_guess, app.py:37-40
| new game | reset w/new game  | still shows old | error in parsing "color:."| app.py:134-138
|          |                   | screen          |                           |
| secret # | You Win message   | Out of attemps! | error in parsing "color:."| app.py:134-138
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? 
Claude

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
The message hints say the opposite of what it should.  In the code, function check_guess in app.py:37-40
•	Symptom: A guess of 80 when the secret is 50 tells you "Go HIGHER!", so following the hints takes you away from the answer.
•	Cause: When guess > secret, the code returns the message "Go HIGHER!" and the label "Too High". It should say "Go LOWER!" there, and the else branch has the same mix-up the other way round.


- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
 AI offer to rework the scoring system. I turn down because it is out of scope for this exercise.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I check the code and played the game a couple of times.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
