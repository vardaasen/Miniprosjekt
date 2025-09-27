# src/apps/t_feature/helpers.py

import sys

# --- Feature Check for t-strings (PEP 750) ---
try:
    from string.templatelib import Template, Interpolation
    T_STRING_AVAILABLE = True
    def t(s): return Template(s) # Helper for creating templates
except ImportError:
    # We don't print a warning here
    # The main app can handle the warning.
    T_STRING_AVAILABLE = False
    class Template:
        def __init__(self, s): self.s = s
        def __str__(self): return self.s
    class Interpolation: pass # Dummy class
    def t(s): return Template(s)
