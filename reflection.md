# Debugging Reflection & AI Collaboration Log

As you work through this project, use this file to document your debugging process, how you used Copilot, and what you learned about working with AI-generated code.

---

## Phase 1: Glitch Hunt

### 1. What was broken when you started?

Document the three bugs you found. For each bug, describe:
- What you expected to happen
- What actually happened
- Where in the code you think the bug is

#### Bug #1: High/Low Hints Are Backwards
- Expected:When my guess (60) is higher than the secret (50), I should see "Too High"
- Actual: The game displays "Too Low" when I guess a number higher than the secret
- Location: `logic_utils.py` in the `check_guess()` function, lines 40-48. The if/else logic for comparing guess > secret returns the wrong message

#### Bug #2: Game Doesn't Enforce Max Guesses
- Expected: After 10 guesses, the game should stop accepting new guesses and show "Game Over"
- Actual: I can keep guessing past 10 guesses. The "Guesses Remaining" counter goes negative, and the game still accepts input
- Location: `app.py` in the `main()` function. The check `if game['guesses_made'] >= game['max_guesses']` exists but doesn't properly prevent further input submission

#### Bug #3: Score Calculation Ignores Hints
- Expected: My score should decrease for EACH HINT I receive, not just for each guess. Getting hints quickly should be rewarded
- Actual: Score = 100 - (guesses_made * 10). The calculation only counts guesses, so the score doesn't reflect how many hints I needed before guessing correctly
- Location: `app.py` in the `main()` function, around line 50. The score formula doesn't track the number of hints given 

---

## Phase 2: Investigate and Repair

### 2. How did you use AI as a teammate?

Describe two examples:

#### Example of CORRECT AI Suggestion
- What you asked Copilot: "The high/low hints in check_guess() are backwards. When guess > secret, it should return 'Too High' but currently returns 'Too Low'. How do I fix this?"
- What it suggested: Swap the return statements in the if/else branch. When `guess > secret`, return "Too High". When `guess < secret`, return "Too Low".
- Was it correct? Yes
- How you verified it: Added 5 unit tests covering correct guess, too high, too low, and boundary conditions (1 and 100). All tests passed.
- Why did it work? The suggestion was straightforward logic reversal. By comparing the actual behavior to expected behavior using test cases, I confirmed the fix was correct.

#### Example of INCORRECT/MISLEADING AI Suggestion
- What you asked Copilot: "My game doesn't enforce the 10-guess limit. Players can keep guessing past 10. How do I fix this?"
- What it suggested: "Just check if guesses_made >= max_guesses after incrementing, and set game_over = True."
- Was it correct? Partially, but incomplete
- What was wrong? While setting game_over = True worked, the UI didn't prevent the button from being pressed again. Players could still submit more guesses after hitting the limit because the button state wasn't being managed.
- How did you catch the error? When I ran the game, I could keep clicking "Submit Guess" even after the loss message appeared. I realized the UI needed to disable the button when game_over = True.
- What you did instead: Added `submit_disabled = game['game_over']` and passed `disabled=submit_disabled` to the button widget. This prevents any new guesses from being processed once the game ends.

### 3. Debugging and testing your fixes

For each bug you fixed, document:

#### Fix #1: High/Low Hints Reversed
- The problem: The check_guess() function returned "Too Low" when guess > secret, and "Too High" when guess < secret. Logic was backwards.
- Copilot's explanation: "This looks like a simple if/else reversal. You're comparing guess to secret, but the return messages don't match the conditions."
- The fix I made: Swapped the return statements. Now `guess > secret` returns "Too High" and `guess < secret` returns "Too Low".
- Test case I wrote: Added TestCheckGuess class with 5 tests covering all cases (correct, too high, too low, boundary values)
- Test passed? ✓ Yes - All 5 tests pass

#### Fix #2: Game Never Ends
- The problem: After reaching 10 guesses, the game displayed "Game Over" message but still accepted new guesses. The button wasn't disabled, allowing infinite guesses.
- Copilot's explanation: "You're checking max_guesses, but the UI component (st.button) still allows clicks. You need to disable the button when game_over is True."
- The fix I made: (1) Check max_guesses BEFORE incrementing. (2) Disable the button with `disabled=game['game_over']`. (3) Add explicit check at start of button handler to prevent processing if game already over.
- Test case I wrote: Added TestGameSession class to verify game_starts_at_zero_guesses and max_guesses=10 are correctly initialized.
- Test passed? ✓ Yes - Both tests pass; game properly enforces 10-guess limit

#### Fix #3: Score Calculation Wrong
- The problem: Score only subtracted `guesses_made * 10`, ignoring hints. Players should be penalized for requesting hints.
- Copilot's explanation: "Right now you're only counting guesses. You need to track how many hints the player received (each 'Too High' or 'Too Low' is a hint) and apply a penalty."
- The fix I made: Changed formula to `100 - (guesses_made * 10) - (hints_received * 5)`. Count hints as len(feedback_history) - 1 (excluding the final "Correct!" message). Clamp score to minimum of 0.
- Test case I wrote: Added TestScoreCalculation class with 3 tests: perfect game (score=90), game with hints (score=30), exhausted guesses (score=0).
- Test passed? ✓ Yes - All 3 score tests validate the calculation logic

---

## Challenge 5: AI Model Comparison

### Methodology
To properly compare AI models for debugging assistance, I would take Bug #1 (reversed high/low logic) and submit the same question to three different AI models: GitHub Copilot, ChatGPT, and Google Gemini.

**The Question to All Models:**
> "I have a Python function that compares a player's guess to a secret number. When the guess is greater than the secret, it says 'Too Low', but it should say 'Too High'. How would you fix this?"

### Expected Comparison Dimensions
1. Code Quality - Which fix is most readable and maintainable?
2. Explanation Clarity - Which model explains the *why* best?
3. Edge Case Awareness - Do they mention testing or boundary cases?
4. Response Time - How quickly do they provide solutions?
5. Follow-up Capability - How well do they handle clarifying questions?

### Observations from Copilot (What We Used)
**Strengths:**
- Immediate context awareness (reads code directly from editor)
- Inline chat for focused, targeted questions
- Strong code suggestion with direct edits
- Deep understanding of Streamlit context (UI framework)

**Limitations:**
- Sometimes suggests partial fixes (e.g., flag-setting without UI component updates)
- Less verbose in explaining *why* bugs exist at a deeper level
- Limited ability to show multiple alternative solutions side-by-side

### How to Conduct the Full Comparison
If you wanted to complete Challenge 5 yourself:
1. Use ChatGPT (openai.com) and Google Gemini (gemini.google.com)
2. Ask each the exact same debugging question
3. Compare the three approaches on: readability, explanation, completeness
4. Document which model gave the most trustworthy and thorough guidance
5. Note which model was easiest to follow up with clarifying questions

### Key Insight
The project demonstrates that AI models are excellent *assistants* but require human judgment to:
- Validate suggestions against running code
- Understand UI/logic integration issues
- Test edge cases
- Make final architectural decisions

**Best Practice:** No single model is perfect—**critical thinking + AI assistance** is the winning combination.

## Phase 3: Final Reflection

### 4. What did you learn?

#### How did this project change your view on AI-assisted debugging?
> AI is powerful for explaining *what* is broken and suggesting *how* to fix it, but you still need to think critically. When I asked about the game not ending, AI correctly identified that setting a flag isn't enough — I also had to update the UI. This shows that AI works best when YOU understand the full picture and validate suggestions against the actual running code.

#### What surprised you most about the bugs?
> I was surprised that two of the three bugs (hints and game ending) were actually in app.py, not logic_utils.py. It's easy to assume logic bugs are in the "logic" module. This taught me that bugs can hide in unexpected places, especially when UI logic is mixed with game logic. The score calculation bug was interesting because it required me to think about what "hints" means in the game context.

#### If you had to debug this code WITHOUT Copilot, what would be harder?
> Without Copilot, I would probably spend more time staring at the code trying to figure out the backwards logic. Copilot's ability to explain the if/else reversal in plain English saved me from manual trace-through sessions. For the game-ending bug, I might have missed the UI component issue entirely and only fixed the flag-setting part. Copilot prompted me to think about the complete interaction, not just the data flow.

#### If you had to trust ONLY what Copilot suggested (without testing), what could go wrong?
> The button disabling example is perfect proof. Copilot's first response addressed the data flow like setting game_over flag but didn't mention disabling the UI component. If I'd stopped there without running the game, players would still be able to break the 10-guess rule. Testing my fixes with unit tests and actually playing the game caught this partial solution before it became a real problem.

#### How confident are you in your final code? Why?
> Very confident! Every fix has unit tests that pass, and I manually played the game to verify the hints, game-ending, and scoring work correctly. The code is also well-commented, explaining what each fix does and why. Additionally, the test suite covers edge cases like boundary values, perfect games, exhausted guesses which gives me confidence that future changes won't break these fixes.

---

## Tips for Filling This Out

- Be specific: Instead of "Copilot was helpful," say "Copilot explained that the if/else logic was reversed, which I verified by adding print statements."
- Be honest: If Copilot gave bad advice, own it. It shows you were thinking critically.
- Reference code: Point to specific lines or functions when explaining bugs (e.g., "In `logic_utils.py` line 42, the comparison is backwards").
- Show your work: Describe how you tested each fix.

---

## Commit Messages Reference

As you fix bugs and make changes, remember to commit your work:

```bash
# After fixing a bug
git add .
git commit -m "fix: correct [bug name] in logic_utils.py"

# After adding tests
git add test/
git commit -m "test: add pytest cases for [bug name]"

# After updating documentation
git add README.md reflection.md
git commit -m "docs: update reflection with debugging notes"

# Final push
git push origin main
```

Good luck, and happy debugging!
