# src/apps/T_Feature_App.py

APPNAVN = "GitHub Repo Manager (t-string Demo)"

def app():
    """
    Bridge to t_feature application.
    """
    # Import the main menu function
    from .t_feature.app import main_menu
    
    # Run it
    main_menu()
