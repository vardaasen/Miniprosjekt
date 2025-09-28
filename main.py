import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from typing import Optional, List, Tuple, Dict, Any, Union
from src.apps import Kristoffer, Willads, Chinh
from src.apps.kalk import Start as Michael
from src.apps import T_Feature_App
from src.utils import main_tui
from src.utils import main_tui as cli
PROSJEKTNAVN = "Mini-prosjekt i Python (Gruppe 5)"

# Tastevalg
APPS: dict = { 
    '1': Michael,
    '2': Chinh,
    '3': T_Feature_App,
    '4': Kristoffer
}

def vis_meny():
    print(f"--- {PROSJEKTNAVN} ---")
    print("Velg program fra hovedmeny:")
    for n, app in APPS.items():
        print(f" {n}. {app.APPNAVN}")
    print(" q. Avslutt program (q / Esc / Ctrl+C).")
    print("-" * (len(PROSJEKTNAVN) + 8))

def main():
    cli.cls() # Tøm terminalen først
    vis_meny()
    while True:
        tast = cli.keypress() # Detekterer hvilken tast blir trykket
        #print(f"Tastetrykk: {tast!r}") # -- For test og feilsøking --

        if tast in APPS:
            APPS[tast].app() # Kjør valgt app

            # Tøm terminal og vis hovedmeny på nytt når app er avsluttet
            cli.cls()
            vis_meny()

        elif tast.lower() in cli.Config.lukk_tast: # 'q', Esc, eller Ctrl+C er trykket
            print("Programmet avsluttes.")
            break

if __name__ == "__main__":
    main()
