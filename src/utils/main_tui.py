import os
import sys
from typing import Optional, Tuple, Callable


# -----------------------------
# CONFIG (constants container)
# -----------------------------

class Config:
    """TUI configuration constants.
    grouped in a class for reuse, and not exposed to the global scope.
    they live in an encapsulated namespace and can be called using
    dot notation like Config.exit_message or Config.Keys.ENTER
    Capital first letter is convention that tell the reader this
    is a class"""

    exit_message = "Trykk 'q', ESC eller Ctrl+C for å gå tilbake."

    class Keys:
        esc = chr(27)
        enter = chr(13)
        backspace = (chr(8), chr(127))  # win vs posix differences
        ctrlc = chr(3)
        # compatibility alias (for teammates)
        ESC = esc
        ENTER = enter
        BACKSPACE = backspace
        CTRLC = ctrlc

    lukk_tast: Tuple[str, ...] = ("q", Keys.esc, Keys.ctrlc)

# -----------------------------
# PUBLIC FUNCTIONS
# -----------------------------
def keypress(valid_keys: Optional[Tuple[str]] = None) -> str:
    """Waits for a key press and returns it as string."""
    while True:
        try:
            pressed = _key()                                      # fast path: read raw key
        except (RuntimeError, OSError):
            try:
                pressed = input()[:1]                             # fallback: first char of typed line
            except (EOFError, KeyboardInterrupt):
                # Ctrl+D/Ctrl+Z (EOF) or Ctrl+C cancel
                return Config.Keys.ctrlc
        if not pressed:
            continue                                              # empty input? wait again
        if valid_keys is None or pressed.lower() in valid_keys:
            return pressed                                        # accept and return the key



def cls() -> None:
    """Clear terminal screen (cross-platform)."""
    os.system("cls" if os.name == "nt" else "clear")


# -----------------------------
# PRIVATE HELPERS
# -----------------------------

def _raw_read_windows() -> Callable[[], str]:
    import msvcrt
    def read_key() -> str:
        key = msvcrt.getch()                 # read raw byte from terminal
        try:
            return key.decode("utf-8")       # decode normal characters
        except UnicodeDecodeError:
            return repr(key)                 # show Python's raw byte representation, example b'\x03' for Ctrl+C
    return read_key

def _raw_read_posix() -> Callable[[], str]:
    import tty
    import termios
    def read_key() -> str:
        fd = sys.stdin.fileno()                                # terminal file descriptor
        settings = termios.tcgetattr(fd)                       # save current terminal mode
        try:
            tty.setraw(fd)                                     # raw mode
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, settings) # restore saved terminal mode
    return read_key

# -----------------------------
# OS-SPECIFIC KEY BINDING
# -----------------------------
# the helpers encapsulates os-specifics and _key() is os-agnostic
if os.name == "nt":  # Windows
    _key_read = _raw_read_windows()

elif os.name == "posix":  # Linux / macOS
    _key_read = _raw_read_posix()
else:
    _key_read = None

def _fallback_read() -> str:
    try:
        return input()[:1]
    except (EOFError, KeyboardInterrupt):
        return Config.Keys.ctrlc
# -----------------------------
# public api
# -----------------------------
def _key() -> str:
    reader = _key_read or _fallback_read
    try:
        return reader()
    except OSError:
        return _fallback_read()

# -----------------------------
# COMPATIBILITY ALIASES (for teammates) as public global variables
# -----------------------------
TAST = Config.Keys               # Michael’s `cli.TAST.ENTER`
LUKK_TAST = Config.lukk_tast     # Kristoffer’s `cli.LUKK_TAST`
LUKK_STR = Config.exit_message   # Kristoffer’s `cli.LUKK_STR`
tastetrykk = keypress            # Kristoffer’s `cli.tastetrykk()`
