# templates/regex_patterns.py
"""
Central repository for regular expressions.
This keeps complex pattern matching logic separate from the main code.
"""

# Example: Pattern to extract a version number.
# From the original script, used to find stable python versions.
STABLE_VERSION_PATTERN = r'[abc]\d*|rc\d*'
