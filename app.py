"""
Number Guessing Game - Built with Streamlit

A simple game where players guess a number between 1-100.
The game provides hints and tracks the number of guesses.
Features persistent high-score tracking (Challenge 2).

NOTE: This code intentionally mixes UI logic with game logic 
and contains bugs for you to find and fix!
"""

import streamlit as st
from logic_utils import parse_guess, check_guess, start_game, load_high_scores, save_high_score, get_best_score


def main():
    """Main application entry point."""
    
    st.title("🎮 Number Guessing Game")
    st.write("I'm thinking of a number between 1 and 100. Can you guess it?")
    
    # Challenge 2: Display high scores in sidebar
    st.sidebar.title("High Scores")
    best_score = get_best_score()
    if best_score:
        st.sidebar.success(f"Best Score: **{best_score['score']}** (in {best_score['guesses']} guesses)")
    else:
        st.sidebar.info("No scores yet. Be the first to play!")
    
    # Display top 10 scores
    scores = load_high_scores()
    if scores:
        st.sidebar.write("### Top Scores")
        for i, score_entry in enumerate(scores[:10], 1):
            st.sidebar.write(f"{i}. Score: {score_entry['score']} ({score_entry['guesses']} guesses)")
    
    # Initialize session state
    if 'game' not in st.session_state:
        st.session_state.game = start_game()
        st.session_state.feedback_history = []
    
    game = st.session_state.game
    
    # Display game status
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Guesses Made", game['guesses_made'])
    with col2:
        st.metric("Guesses Remaining", game['max_guesses'] - game['guesses_made'])
    
    # Player input
    guess_input = st.text_input("Enter your guess:", key="guess_input")
    
    # Disable input if game is over
    submit_disabled = game['game_over']
    
    if st.button("Submit Guess", disabled=submit_disabled):
        # FIX #2: Check if game is already over before processing new guesses
        if game['game_over']:
            st.warning("Game is over! Click 'Reset Game' to play again.")
        else:
            # Parse the input
            guess = parse_guess(guess_input)
            
            if guess is None:
                st.error("Please enter a valid number between 1 and 100.")
            else:
                # FIX #2: Check max guesses BEFORE incrementing, not after
                if game['guesses_made'] >= game['max_guesses']:
                    st.error(f"Game Over! You've used all {game['max_guesses']} guesses. The secret number was {game['secret']}")
                    game['game_over'] = True
                else:
                    game['guesses_made'] += 1
                    
                    # Get feedback from logic
                    feedback = check_guess(guess, game['secret'])
                    st.session_state.feedback_history.append((guess, feedback))
                    
                    # Display feedback
                    if feedback == "Correct!":
                        st.success(f"🎉 You got it! The number was {game['secret']}!")
                        st.balloons()
                        game['game_over'] = True
                        
                        # FIX #3: Score calculation now accounts for hints received
                        # Each hint counts as a -5 point penalty, each guess as -10 points
                        hints_received = len(st.session_state.feedback_history) - 1  # Don't count "Correct!"
                        score = 100 - (game['guesses_made'] * 10) - (hints_received * 5)
                        score = max(0, score)  # Ensure score doesn't go negative
                        st.write(f"**Your Score:** {score}")
                        
                        # Challenge 2: Save the high score to persistent storage
                        save_high_score(score, game['guesses_made'])
                        st.success(f"✨ Score saved! Check the sidebar for high scores.")
                        
                        # Challenge 4: Display game statistics and summary table
                        st.write("### 📊 Game Statistics")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Guesses Used", game['guesses_made'])
                        with col2:
                            st.metric("Hints Received", hints_received)
                        with col3:
                            accuracy = (1 - (hints_received / max(1, game['guesses_made']))) * 100
                            st.metric("Accuracy", f"{accuracy:.0f}%")
                        
                        # Challenge 4: Summary table of all guesses
                        st.write("### 📋 Guess Summary")
                        guess_data = []
                        for idx, (g, f) in enumerate(st.session_state.feedback_history, 1):
                            distance = abs(g - game['secret'])
                            guess_data.append({
                                "Guess #": idx,
                                "Number": g,
                                "Feedback": f,
                                "Distance": distance if f != "Correct!" else 0
                            })
                        
                        import pandas as pd
                        df = pd.DataFrame(guess_data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        # Challenge 4: Enhanced feedback with hot/cold indicator
                        distance = abs(guess - game['secret'])
                        
                        if distance <= 5:
                            st.error(f"🔥 {feedback} (HOT! Only {distance} away!)")
                        elif distance <= 10:
                            st.warning(f"🌡️ {feedback} (WARM - {distance} away)")
                        else:
                            st.info(f"❄️ {feedback} (COLD - {distance} away)")
                        
                        # FIX #2: Properly check if max guesses reached after this guess
                        if game['guesses_made'] >= game['max_guesses']:
                            st.error(f"Game Over! You've used all {game['max_guesses']} guesses. The secret number was {game['secret']}")
                            game['game_over'] = True
    
    # Display feedback history
    if st.session_state.feedback_history:
        st.write("### Your Guesses:")
        for guess, feedback in st.session_state.feedback_history:
            st.write(f"- Guessed: **{guess}** → {feedback}")
    
    # Reset button
    if st.button("Reset Game"):
        st.session_state.game = start_game()
        st.session_state.feedback_history = []
        st.rerun()


if __name__ == "__main__":
    main()