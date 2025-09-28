import os
import sqlite3
from contextlib import contextmanager

from .templates import sql_queries, log_messages

class DatabaseManager:
    """Wrapper around the SQLite calls in the app"""
    def __init__(self, logger, db_path="repos.db"):
        self.db_path = db_path
        self.logger = logger

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)                          # opens a connection
        try:
            yield conn
        finally:
            conn.close()                                              # always close connection

                                                                      # start with a clean db file

    def _new_clean_db(self):
        if os.path.exists(self.db_path):                              # helper function help make the code
            os.remove(self.db_path)                                   # easier to read

    def _create_repo_table(self, conn):
        cursor = conn.cursor()                                        # and understand
        cursor.execute(sql_queries.CREATE_REPOS_TABLE)
        conn.commit()                                                 # can't be perfect
        self.logger.info(log_messages.DB_SETUP_COMPLETE,
            db_path=self.db_path)                                     # try to avoid long lines

    """create the repo table"""
    def setup(self):
        self._new_clean_db()
        with self.get_connection() as conn:
            self._create_repo_table(conn)
                                                                      # student helper function
    def _create_students_table(self, conn):
        cursor = conn.cursor()
        cursor.execute(sql_queries.CREATE_STUDENTS_TABLE)
        cursor = conn.cursor()
        cursor.executemany(sql_queries.INSERT_STUDENT,
                           sql_queries.SAMPLE_STUDENTS)
        conn.commit()

    """create the students table"""
    def setup_students(self):
        self._new_clean_db()
        with self.get_connection() as conn:
            self._create_students_table(conn)


    def _store_repos(self, conn, repo_data):
        cursor = conn.cursor()
        cursor.executemany(sql_queries.INSERT_REPO, repo_data)
        conn.commit()
        self.logger.info(log_messages.REPOS_STORED,
                         count=len(repo_data))

    def store_repos(self, repos):
        repo_data = [
            (
                r.get('name'),
                r.get('full_name'),
                r.get('html_url'),
                r.get('description'),
                r.get('language'),
                r.get('stargazers_count', 0)
            )
            for r in repos
        ]
        with self.get_connection() as conn:
            self._store_repos(conn, repo_data)

    def _search_repos(self, conn, term):
        cursor = conn.cursor()
        cursor.execute(sql_queries.SEARCH_REPOS,
                       (f"%{term}%", f"%{term}%"))
        results = cursor.fetchall()
        self.logger.info(log_messages.SEARCH_COMPLETE,
                         count=len(results),
                         term=term)

    def search_repos(self, term):
        with self.get_connection() as conn:
            return self._search_repos(conn, term)


    def search_safe(self, term, show_query=False):
        with self.get_connection() as conn:
            if show_query:
                print(f"SQL: {sql_queries.SEARCH_STUDENTS_SAFE}")
                print(f"Param: {f'%{term}%'!r}")
            cursor = conn.cursor()
            cursor.execute(sql_queries.SEARCH_STUDENTS_SAFE,
                           (f"%{term}%",))
            results = cursor.fetchall()
            if show_query:
                print(f"Results: {results}")
            return results

    def search_vulnerable_real(self, term, show_query=False):
        """Really vulnerable - uses executescript to allow multiple statements"""
        query = sql_queries.SEARCH_STUDENTS_VULNERABLE.format(term=term)
        if show_query:
            print(f"SQL: {query}")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.executescript(query)
                # Try to get results if table still exists
                try:
                    cursor.execute(sql_queries.SELECT_STUDENT_ROBERT)
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
        query = sql_queries.SEARCH_STUDENTS_VULNERABLE.format(term=term)
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
            cursor.execute(sql_queries.LIST_TABLES)
            return [row[0] for row in cursor.fetchall()]

    def show_table_info(self, table="students"):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_queries.TABLE_SCHEMA.format(table=table))
            schema = cursor.fetchone()
            if schema:
                print(f"Schema: {schema[0]}")
            cursor.execute(sql_queries.TABLE_ROWS.format(table=table))
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                print(f"Row {i}: {row}")
