# app.py
import sqlite3
import urllib.request
import urllib.error
import json
import logging
import os
import sys
from string import Template
from contextlib import contextmanager

from .templates import sql_queries, log_messages
from ...utils import cli
from .helpers import t, T_STRING_AVAILABLE

if not T_STRING_AVAILABLE:
    print("WARNING: Python < 3.14. t-string features disabled.", file=sys.stderr)


class Logger:
    def __init__(self, verbose_level=0):
        self.verbose_level = verbose_level
        log_level = [logging.WARNING, logging.INFO, logging.DEBUG][min(verbose_level, 2)]
        logging.basicConfig(
            level=log_level,
            format='%(levelname)s: %(message)s',
            stream=sys.stdout
        )
        self.logger = logging.getLogger(__name__)

    def _format_msg(self, template, **kwargs):
        if T_STRING_AVAILABLE:
            return str(template)
        return template.s.format(**kwargs)

    def info(self, template, **kwargs):
        if self.verbose_level >= 1:
            if self.verbose_level >= 2:
                print(f"Template: {template!r}, kwargs: {kwargs!r}")
            self.logger.info(self._format_msg(template, **kwargs))

    def error(self, template, **kwargs):
        self.logger.error(self._format_msg(template, **kwargs))


class DatabaseManager:
    def __init__(self, logger, db_path="repos.db"):
        self.db_path = db_path
        self.logger = logger

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def setup(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        with self.get_connection() as conn:
            conn.cursor().execute(sql_queries.CREATE_REPOS_TABLE)
            conn.commit()
            self.logger.info(log_messages.DB_SETUP_COMPLETE, db_path=self.db_path)

    def setup_students(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        with self.get_connection() as conn:
            conn.cursor().execute(sql_queries.CREATE_STUDENTS_TABLE)
            conn.cursor().executemany(sql_queries.INSERT_STUDENT, sql_queries.SAMPLE_STUDENTS)
            conn.commit()

    def store_repos(self, repos):
        with self.get_connection() as conn:
            repo_data = [(r.get('name'), r.get('full_name'), r.get('html_url'),
                          r.get('description'), r.get('language'), r.get('stargazers_count', 0))
                         for r in repos]
            conn.cursor().executemany(sql_queries.INSERT_REPO, repo_data)
            conn.commit()
            self.logger.info(log_messages.REPOS_STORED, count=len(repo_data))

    def search_repos(self, term):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_queries.SEARCH_REPOS, (f"%{term}%", f"%{term}%"))
            results = cursor.fetchall()
            self.logger.info(log_messages.SEARCH_COMPLETE, count=len(results), term=term)
            return results

    def search_safe(self, term, show_query=False):
        with self.get_connection() as conn:
            if show_query:
                print(f"SQL: {sql_queries.SEARCH_STUDENTS_SAFE}")
                print(f"Param: {f'%{term}%'!r}")
            cursor = conn.cursor()
            cursor.execute(sql_queries.SEARCH_STUDENTS_SAFE, (f"%{term}%",))
            results = cursor.fetchall()
            if show_query:
                print(f"Results: {results}")
            return results

    def search_vulnerable_real(self, term, show_query=False):
        """Really vulnerable - uses executescript to allow multiple statements"""
        query = f"SELECT name, grade, email FROM students WHERE name LIKE '%{term}%'"
        if show_query:
            print(f"SQL: {query}")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.executescript(query)
                # Try to get results if table still exists
                try:
                    cursor.execute("SELECT name, grade, email FROM students WHERE name LIKE '%Robert%'")
                    results = cursor.fetchall()
                except sqlite3.Error:
                    results = "TABLE_DESTROYED"
                if show_query:
                    print(f"Results: {results}")
                return results
            except sqlite3.Error as e:
                if show_query:
                    print(f"Error: {e}")
                return None

    def search_vulnerable(self, term, show_query=False):
        """Vulnerable code but Python's execute() provides some protection"""
        query = f"SELECT name, grade, email FROM students WHERE name LIKE '%{term}%'"
        if show_query:
            print(f"SQL: {query}")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                results = cursor.fetchall()
                if show_query:
                    print(f"Results: {results}")
                return results
            except sqlite3.Error as e:
                if show_query:
                    print(f"Error: {e}")
                return None

    def list_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in cursor.fetchall()]

    def show_table_info(self, table="students"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE name = '{table}'")
            schema = cursor.fetchone()
            if schema:
                print(f"Schema: {schema[0]}")
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                print(f"Row {i}: {row}")


class GitHubClient:
    def __init__(self, logger, token=None):
        self.logger = logger
        self.headers = {'User-Agent': 'SimpleGitHubManager/3.0'}
        if token:
            self.headers['Authorization'] = f'Bearer {token}'

    def fetch_repos(self, username, limit=10):
        url = f"https://api.github.com/users/{username}/repos?per_page={limit}"
        self.logger.info(log_messages.FETCHING_REPOS, url=url)
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode())
                    self.logger.info(log_messages.FETCH_SUCCESS, count=len(data), username=username)
                    return data
                self.logger.error(log_messages.FETCH_HTTP_ERROR, status=response.status)
                return None
        except Exception as e:
            self.logger.error(log_messages.FETCH_GENERAL_ERROR, error=str(e))
            return None


class AppManager:
    def __init__(self, verbose_level=0):
        self.logger = Logger(verbose_level)
        self.db = DatabaseManager(self.logger)
        self.client = GitHubClient(self.logger, os.getenv('GITHUB_TOKEN'))

    def run_search(self, username, search_term):
        print(f"Search: {username}/{search_term}")
        self.db.setup()
        repos = self.client.fetch_repos(username)
        if repos:
            self.db.store_repos(repos)
            results = self.db.search_repos(search_term)
            self._show_results(results, search_term)
        else:
            print("No repos fetched")

    def _show_results(self, results, term):
        print(f"Matches for '{term}':")
        for name, url, desc in results[:5]:
            desc = (desc[:50] + '...') if desc and len(desc) > 50 else (desc or "No desc")
            print(f"{name}: {desc}")

    def demo_security(self):
        print("♜ SQL INJECTION DEMO")
        print(f"T_STRING_AVAILABLE: {T_STRING_AVAILABLE}")

        bobby = "Robert'; DROP TABLE students; --"
        print(f"Attack string: {bobby!r}")

        # Method 1: Truly vulnerable (executescript)
        print("\n1. FULLY VULNERABLE (executescript)")
        self.db.setup_students()
        self.db.search_vulnerable_real("Alice", True)
        self.db.search_vulnerable_real(bobby, True)
        tables_1 = self.db.list_tables()
        print(f"Tables remaining: {tables_1}")
        result_1 = 'DESTROYED' if 'students' not in tables_1 else 'INTACT'

        # Method 2: Vulnerable code but Python's protection
        print("\n2. VULNERABLE CODE + PYTHON PROTECTION (execute)")
        self.db.setup_students()
        self.db.search_vulnerable("Alice", True)
        self.db.search_vulnerable(bobby, True)
        tables_2 = self.db.list_tables()
        print(f"Tables remaining: {tables_2}")
        result_2 = 'PROTECTED' if 'students' in tables_2 else 'DESTROYED'

        # Method 3: Proper safe approach
        print("\n3. SAFE PARAMETERIZED (template/t-string approach)")
        self.db.setup_students()
        print(f"Template: {t('query with {param}')!r}")
        self.db.search_safe("Alice", True)
        self.db.search_safe(bobby, True)
        tables_3 = self.db.list_tables()
        print(f"Tables remaining: {tables_3}")
        result_3 = 'SAFE' if 'students' in tables_3 else 'ERROR'

        print("\nRESULTS:")
        print(f"1. executescript():     {result_1}")
        print(f"2. execute():          {result_2}")
        print(f"3. parameterized:      {result_3}")
        print("\nPython's execute() helps, but proper parameterization is the real solution")


def main_menu():
    while True:
        cli.cls()
        print("GitHub Repository Manager")
        print("1. Quick Search")
        print("2. Verbose Search")
        print("3. Custom Search")
        print("4. SQL Security Demo")
        print(f"\n{cli.LUKK_STR}")

        key = cli.keypress()
        if key.lower() in cli.LUKK_TAST:
            break

        cli.cls()
        if key == '1':
            AppManager(0).run_search('octocat', 'hello')
        elif key == '2':
            AppManager(1).run_search('octocat', 'hello')
        elif key == '3':
            try:
                user = input("Username [octocat]: ").strip() or 'octocat'
                term = input("Search term [hello]: ").strip() or 'hello'
                AppManager(1).run_search(user, term)
            except (KeyboardInterrupt, EOFError):
                print("Cancelled")
        elif key == '4':
            AppManager(0).demo_security()

        print(f"\n{cli.LUKK_STR}")
        cli.keypress()


if __name__ == "__main__":
    main_menu()