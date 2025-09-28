import os
import sys
from typing import Optional, Tuple


# -----------------------------
# CONFIG (constants container)
# -----------------------------

class Config:
    """CLI configuration constants."""

    exit_message = "Trykk 'q', ESC eller Ctrl+C for å gå tilbake."

    class Keys:
        esc = chr(27)
        enter = chr(13)
        backspace = (chr(8), chr(127))  # win vs posix differences
        ctrlc = chr(3)
        ESC = esc
        ENTER = enter
        BACKSPACE = backspace
        CTRLC = ctrlc

    lukk_tast: Tuple[str, ...] = ("q", Keys.esc, Keys.ctrlc)

# it is a better pattern to check features than platform
# but throughout this script we do platform check anyway
# -----------------------------
# OS-SPECIFIC KEY BINDING
# -----------------------------
if os.name == "nt":  # Windows
    import msvcrt

    def _key() -> str:
        return _key_windows()

elif os.name == "posix":  # Linux / macOS
    import tty, termios

    def _key() -> str:
        return _key_posix()

else:
    raise RuntimeError("Operativsystemet støttes ikke.")


# -----------------------------
# PUBLIC FUNCTIONS
# -----------------------------
def keypress(valid_keys: Optional[Tuple[str]] = None) -> str:
    """Waits for a key press and returns it as string."""
    while True:
        pressed = _key()

        if valid_keys is None:
            return pressed

        if pressed.lower() in valid_keys:
            return pressed


def cls() -> None:
    """Clear terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


# -----------------------------
# PRIVATE HELPERS
# -----------------------------
def _key_windows() -> str:
    """Windows: blocking key detection using msvcrt."""
    key = msvcrt.getch()  # bytes
    try:
        return key.decode("utf-8")
    except UnicodeDecodeError:
        return repr(key)


def _key_posix() -> str:
    """POSIX (Linux/macOS): blocking key detection (no enter needed)."""
    terminal = sys.stdin.fileno()
    settings = termios.tcgetattr(terminal)
    try:
        tty.setraw(terminal)
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(terminal, termios.TCSADRAIN, settings)
    return char


# -----------------------------
# COMPATIBILITY ALIASES (for teammates)
# -----------------------------
TAST = Config.Keys               # Michael’s `cli.TAST.ENTER`
LUKK_TAST = Config.lukk_tast     # Kristoffer’s `cli.LUKK_TAST`
LUKK_STR = Config.exit_message   # Kristoffer’s `cli.LUKK_STR`
tastetrykk = keypress            # Kristoffer’s `cli.tastetrykk()`
