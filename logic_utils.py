"""
Game logic module for the Number Guessing Game.

This module provides core game logic functions for a simple number guessing game
where players attempt to guess a secret number between 1 and 100 within 10 attempts.

Functions:
    parse_guess: Validates and converts user input string to integer
    check_guess: Compares player guess to secret number
    start_game: Initializes a new game session
    load_high_scores: Retrieves persistent high scores from disk
    save_high_score: Saves a new high score to persistent storage
    get_best_score: Gets the top score of all time

Challenge 2 Enhancement: Includes persistent high scores stored in scores.json
Challenge 3 Enhancement: Professional-grade docstrings with examples

Version: 2.0
"""

import random
import json
from pathlib import Path


def load_high_scores():
    """
    Load high scores from persistent storage (scores.json file).
    
    Reads the scores.json file from the current directory and returns all
    saved high scores. Gracefully handles missing files or corrupted JSON
    by returning an empty list.
    
    File Format:
        Location: ./scores.json in the app's working directory
        Format: JSON array of objects with 'score' and 'guesses' fields
        Auto-created by save_high_score() on first game completion
    
    Challenge 2: Part of persistent scoring across game sessions.
    
    Returns:
        list: List of score dictionaries, each containing:
            - 'score' (int): Points achieved (0-100+ range)
            - 'guesses' (int): Number of guesses used to win (1-10)
            List is empty [] if scores.json doesn't exist or is invalid.
            
    Example:
        >>> scores = load_high_scores()
        >>> len(scores) <= 10
        True
        >>> if scores:
        ...     print(f"Best score: {scores[0]['score']}")
    """
    scores_file = Path("scores.json")
    if scores_file.exists():
        try:
            with open(scores_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_high_score(score, guesses):
    """
    Save a new high score to persistent storage (scores.json file).
    
    Appends the new score to the high scores list and maintains top 10 scores
    in descending order by score value. File is created if it doesn't exist.
    Only the top 10 scores are retained; older low scores are discarded.
    
    Challenge 2: Enables score persistence for the high score tracker.
    
    Args:
        score (int): The player's final score (0-100+ range, uncapped)
        guesses (int): Number of guesses it took to win (expected 1-10)
        
    Returns:
        None
        
    Side Effects:
        - Creates or updates ./scores.json with current high scores
        - Scores are sorted in descending order by score value
        - Only top 10 scores are retained; older scores may be dropped
        
    Example:
        >>> save_high_score(95, 3)  # Won in 3 guesses, 95 points
        >>> # scores.json is now created/updated
    """
    scores = load_high_scores()
    scores.append({"score": score, "guesses": guesses})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep top 10 scores
    
    with open("scores.json", "w") as f:
        json.dump(scores, f, indent=2)


def get_best_score():
    """
    Get the highest score achieved across all game sessions.
    
    Retrieves the top entry from the high scores list. Useful for displaying
    a player's best achievement or comparing against a target score.
    
    Challenge 2: Part of high score tracking system.
    
    Returns:
        dict or None: Dictionary with keys:
            - 'score' (int): Best score achieved
            - 'guesses' (int): Guesses used in that winning game
            Returns None if no scores have been saved yet.
            
    Example:
        >>> best = get_best_score()
        >>> if best:
        ...     print(f"Best: {best['score']} in {best['guesses']} guesses")
        ... else:
        ...     print("No games completed yet")
    """
    scores = load_high_scores()
    return scores[0] if scores else None


def parse_guess(guess_str):
    """
    Parse a string input into an integer guess.
    
    Validates that the input is a valid integer within the game's range (1-100).
    Handles non-numeric strings, out-of-range values, decimals, negatives, and 
    empty strings gracefully by returning None.
    
    Args:
        guess_str (str): The user's input as a string (whitespace is stripped)
        
    Returns:
        int: The parsed integer (1-100) if valid, or None if invalid
        
    Examples:
        >>> parse_guess("42")
        42
        >>> parse_guess("101")
        None
        >>> parse_guess("  50  ")
        50
    """
    try:
        guess = int(guess_str.strip())
        if guess < 1 or guess > 100:
            return None
        return guess
    except ValueError:
        return None


def check_guess(guess, secret):
    """
    Check the user's guess against the secret number.
    
    Compares the guessed number to the secret number and returns appropriate feedback.
    This is the core game logic function that provides hints to the player.
    
    BUG FIX #1: Originally had reversed logic, saying "Too Low" when guess was too high.
    This has been corrected to provide accurate feedback.
    
    Args:
        guess (int): The user's guess
        secret (int): The secret number to guess
        
    Returns:
        str: Feedback message ("Correct!", "Too High", or "Too Low")
        
    Examples:
        >>> check_guess(50, 50)
        'Correct!'
        >>> check_guess(60, 50)
        'Too High'
        >>> check_guess(40, 50)
        'Too Low'
    """
    if guess == secret:
        return "Correct!"
    elif guess > secret:
        # FIX #1: Corrected reversed logic - now correctly returns "Too High" when guess is greater
        return "Too High"
    else:
        # FIX #1: Corrected reversed logic - now correctly returns "Too Low" when guess is less
        return "Too Low"


def start_game():
    """
    Initialize a new game session.
    
    Creates a fresh game state dictionary with all necessary variables to track
    the current game. Each call generates a new random secret number and resets
    all game counters.
    
    Game Rules:
    - Secret number is randomly chosen between 1 and 100 (inclusive)
    - Player has exactly 10 guesses to find the number
    - Game ends when player guesses correctly or reaches 10 guesses
    
    BUG FIX #2: The base game state is initialized correctly here. The bug was in
    the UI layer (app.py) not properly enforcing the 10-guess limit.
    
    Returns:
        dict: A dictionary with keys:
            - 'secret' (int): The random number (1-100) to guess
            - 'max_guesses' (int): Maximum number of guesses allowed (always 10)
            - 'guesses_made' (int): Counter for guesses so far (starts at 0)
            - 'game_over' (bool): Boolean flag for game end status (starts as False)
            
    Example:
        >>> game = start_game()
        >>> 1 <= game['secret'] <= 100
        True
        >>> game['guesses_made']
        0
        >>> game['max_guesses']
        10
    """
    return {
        'secret': random.randint(1, 100),
        'max_guesses': 10,
        'guesses_made': 0,
        'game_over': False
    }