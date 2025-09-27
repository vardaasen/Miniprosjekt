# src/apps/T_Feature_App.py

# A descriptive name for the main menu
APPNAVN = "GitHub Repo Manager (t-string Demo)"

def app():
    """
    This function acts as the bridge to your t_feature application.
    """
    # Import the main menu function from your app
    from .t_feature.app import main_menu
    
    # Run it
    main_menu()
