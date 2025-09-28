# templates/sql_queries.py
"""
Central repository for all SQL statements used in the application.
By keeping them here, the code is easier to read
"""

# Repository table
CREATE_REPOS_TABLE = """
CREATE TABLE IF NOT EXISTS repositories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    full_name TEXT UNIQUE NOT NULL,
    html_url TEXT,
    description TEXT,
    language TEXT,
    stars INTEGER DEFAULT 0
)
"""

INSERT_REPO = """
INSERT OR IGNORE INTO repositories (name, full_name, html_url, description, language, stars)
VALUES (?, ?, ?, ?, ?, ?)
"""

SEARCH_REPOS = """
SELECT name, html_url, description
FROM repositories
WHERE name LIKE ? OR description LIKE ?
ORDER BY stars DESC
"""

# Students table for security demo
CREATE_STUDENTS_TABLE = """
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    grade TEXT,
    email TEXT
)
"""

INSERT_STUDENT = "INSERT INTO students (name, grade, email) VALUES (?, ?, ?)"

SEARCH_STUDENTS_SAFE = "SELECT name, grade, email FROM students WHERE name LIKE ?"

# Sample data
SAMPLE_STUDENTS = [
    ("Alice Johnson", "A", "alice@school.edu"),
    ("Bob Smith", "B+", "bob@school.edu"),
    ("Charlie Brown", "A-", "charlie@school.edu"),
    ("Diana Prince", "A", "diana@school.edu")
]

SEARCH_STUDENTS_VULNERABLE = "SELECT name, grade, email FROM students WHERE name LIKE '%{term}%'"
SELECT_STUDENT_ROBERT = "SELECT name, grade, email FROM students WHERE name LIKE '%Robert%'"
LIST_TABLES = "SELECT name FROM sqlite_master WHERE type='table'"
TABLE_SCHEMA = "SELECT sql FROM sqlite_master WHERE name = '{table}'"
TABLE_ROWS = "SELECT * FROM {table}"