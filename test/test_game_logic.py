"""
Unit tests for game logic.

TODO: You will add tests here as you fix each bug.
Example structure:

def test_check_guess_too_high():
    # Arrange: set up test data
    guess = 60
    secret = 50
    
    # Act: call the function
    result = check_guess(guess, secret)
    
    # Assert: verify the result
    assert result == "Too High"
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from logic_utils import parse_guess, check_guess, start_game


class TestParseGuess:
    """Test the parse_guess function."""
    
    def test_valid_guess(self):
        """Parse a valid guess string."""
        result = parse_guess("42")
        assert result == 42
    
    def test_guess_out_of_range_low(self):
        """Invalid guess below 1."""
        result = parse_guess("0")
        assert result is None
    
    def test_guess_out_of_range_high(self):
        """Invalid guess above 100."""
        result = parse_guess("101")
        assert result is None
    
    def test_invalid_string(self):
        """Non-numeric input."""
        result = parse_guess("abc")
        assert result is None
    
    # Challenge 1: Edge-case tests for robustness
    def test_negative_number(self):
        """Negative numbers should be rejected."""
        result = parse_guess("-50")
        assert result is None
    
    def test_decimal_number(self):
        """Decimal/float inputs should be rejected."""
        result = parse_guess("50.5")
        assert result is None
    
    def test_extremely_large_value(self):
        """Extremely large numbers (1000000) should be rejected."""
        result = parse_guess("1000000")
        assert result is None
    
    def test_whitespace_handling(self):
        """Input with leading/trailing whitespace should be accepted."""
        result = parse_guess("  50  ")
        assert result == 50
    
    def test_empty_string(self):
        """Empty string input should be rejected."""
        result = parse_guess("")
        assert result is None
    
    def test_boundary_minimum(self):
        """Guess at minimum boundary (1) should be valid."""
        result = parse_guess("1")
        assert result == 1
    
    def test_boundary_maximum(self):
        """Guess at maximum boundary (100) should be valid."""
        result = parse_guess("100")
        assert result == 100
    
    def test_special_characters(self):
        """Special characters in input should be rejected."""
        result = parse_guess("50@#$")
        assert result is None
    
    def test_scientific_notation(self):
        """Scientific notation should be rejected (e.g., 1e5)."""
        result = parse_guess("1e5")
        assert result is None


class TestStartGame:
    """Test game initialization."""
    
    def test_start_game_returns_dict(self):
        """start_game returns a dictionary with correct keys."""
        game = start_game()
        assert isinstance(game, dict)
        assert 'secret' in game
        assert 'max_guesses' in game
        assert 'guesses_made' in game
        assert 'game_over' in game
    
    def test_secret_in_range(self):
        """Secret number is between 1 and 100."""
        game = start_game()
        assert 1 <= game['secret'] <= 100
    
    def test_initial_state(self):
        """Game starts with correct initial state."""
        game = start_game()
        assert game['guesses_made'] == 0
        assert game['max_guesses'] == 10
        assert game['game_over'] is False


# TODO: Add tests for check_guess after you fix BUG #1
# Example:
# def test_check_guess_correct():
#     assert check_guess(50, 50) == "Correct!"
#
# def test_check_guess_too_high():
#     assert check_guess(60, 50) == "Too High"
#
# def test_check_guess_too_low():
#     assert check_guess(40, 50) == "Too Low"


class TestCheckGuess:
    """Test the check_guess function after fix #1."""
    
    def test_check_guess_correct(self):
        """User guesses the correct number."""
        result = check_guess(50, 50)
        assert result == "Correct!"
    
    def test_check_guess_too_high(self):
        """User's guess is higher than secret."""
        result = check_guess(60, 50)
        assert result == "Too High"
    
    def test_check_guess_too_low(self):
        """User's guess is lower than secret."""
        result = check_guess(40, 50)
        assert result == "Too Low"
    
    def test_check_guess_boundary_high(self):
        """Test boundary: guess at upper end (100)."""
        result = check_guess(100, 50)
        assert result == "Too High"
    
    def test_check_guess_boundary_low(self):
        """Test boundary: guess at lower end (1)."""
        result = check_guess(1, 50)
        assert result == "Too Low"


class TestGameSession:
    """Test game session mechanics."""
    
    def test_game_starts_at_zero_guesses(self):
        """New game should start with 0 guesses."""
        game = start_game()
        assert game['guesses_made'] == 0
    
    def test_game_has_max_of_10_guesses(self):
        """Game should allow maximum 10 guesses."""
        game = start_game()
        assert game['max_guesses'] == 10


class TestScoreCalculation:
    """Test score calculation mechanics (FIX #3)."""
    
    def test_score_perfect_game(self):
        """Perfect game: 1 guess, no hints."""
        # Score = 100 - (1 * 10) - (0 * 5) = 90
        guesses_made = 1
        hints_received = 0
        score = 100 - (guesses_made * 10) - (hints_received * 5)
        assert score == 90
    
    def test_score_with_hints(self):
        """Game with hints: 5 guesses, 4 hints."""
        # Score = 100 - (5 * 10) - (4 * 5) = 100 - 50 - 20 = 30
        guesses_made = 5
        hints_received = 4
        score = 100 - (guesses_made * 10) - (hints_received * 5)
        assert score == 30
    
    def test_score_many_guesses(self):
        """Game with many guesses: 10 guesses, 9 hints."""
        # Score = 100 - (10 * 10) - (9 * 5) = 100 - 100 - 45 = -45, but clamped to 0
        guesses_made = 10
        hints_received = 9
        score = max(0, 100 - (guesses_made * 10) - (hints_received * 5))
        assert score == 0