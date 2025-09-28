# app.py
import urllib.request
import urllib.error
import json
import os
import sys



# local imports
from .templates import sql_queries, log_messages
from .helpers import t, T_STRING_AVAILABLE
from ...utils import main_tui
from .logger import Logger
from .databasemanager import DatabaseManager

# asking the helpers.py if t-string features are available
if not T_STRING_AVAILABLE:
    print("WARNING: Python < 3.14. t-string features disabled.", file=sys.stderr)





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
        main_tui.cls()
        print("GitHub Repository Manager")
        print("1. Quick Search")
        print("2. Verbose Search")
        print("3. Custom Search")
        print("4. SQL Security Demo")
        print(f"\n{main_tui.LUKK_STR}")

        key = main_tui.keypress()
        if key.lower() in main_tui.LUKK_TAST:
            break

        main_tui.cls()
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

        print(f"\n{main_tui.LUKK_STR}")
        main_tui.keypress()


if __name__ == "__main__":
    main_menu()