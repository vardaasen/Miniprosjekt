# src/utils/cli.py
"""
A mock command-line interface (CLI) utility module.
This provides the necessary functions for the menu system in app.py to run,
allowing for a standalone demonstration without a larger framework.
"""
import os

# -- Configuration for menu interaction --

# A string displayed to prompt the user to continue.
LUKK_STR = "Press any key to continue..."

# A set of keys that will exit the main menu loop.
LUKK_TAST = {'q', 'x'}


def cls():
    """
    Clears the console screen.
    Works on both Windows ('nt') and POSIX-compliant systems ('posix').
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def keypress() -> str:
    """
    Waits for and captures a single keypress from the user.
    Returns the first character of the user's input.
    """
    try:
        return input()[:1]
    except (EOFError, KeyboardInterrupt):
        # If the user signals to exit (e.g., Ctrl+C), return a 'q'
        # to ensure the main loop can terminate gracefully.
        print("\nExiting.")
        return 'q'
