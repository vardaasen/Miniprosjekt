from src.utils import cli
from src.apps.t_feature import app

APPNAVN = "Github API | Willads"


def app():
    """Main app entry point - uses clean package interface."""
    cli.cls()
    print(f"--- {APPNAVN} ---")
    print("GitHub Repository Search")
    print()
    print("Features:")
    print("• GitHub API integration")
    print("• Repository search by name/description")
    print("• Clean CLI integration")
    print()
    print(cli.LUKK_STR)
    print("-" * (len(APPNAVN) + 8))

    app()  # Clean exit back to main CLI