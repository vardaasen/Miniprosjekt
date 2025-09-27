# templates/log_messages.py
"""
Central repository for t-string log message templates.
This approach separates logging content from application logic.
On Python < 3.14, these are processed by a fallback string formatter.
"""
from ..helpers import t # Go up one level to 't_feature' and find helpers.py

# Database operations
DB_SETUP_COMPLETE = t("Database setup complete | path={db_path}")
REPOS_STORED = t("Repositories stored in database | count={count}")
SEARCH_COMPLETE = t("Search completed | count={count}, term={term}")

# GitHub API operations
FETCHING_REPOS = t("Fetching repositories from GitHub API | url={url}")
FETCH_SUCCESS = t("Successfully fetched repositories | count={count}, username={username}")
FETCH_HTTP_ERROR = t("GitHub API returned an error | status={status}")
FETCH_GENERAL_ERROR = t("An error occurred during fetch | error={error}")
