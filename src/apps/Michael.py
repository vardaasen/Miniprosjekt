from utils import cli

APPNAVN = "Kalkulator | Michael"

def app():
    cli.cls() # Tøm terminal
    print(f"--- {APPNAVN} ---")
    print("Skriv inn hele regnestykket ditt og trykk Enter for utregning.")
    print("\n" + cli.LUKK_STR)
    print("-" * (len(APPNAVN) + 8))
    uttrykk = ""
    while True:
        print(f"\r\033[K> {uttrykk}", end="")  # Fastholde linje for matteuttrykk i terminal uten linjeskift ved inntasting, og sørger for at tegn slettes fra markøren når man bruker Backspace ved hjelp av Escape-kommando '\033[K' (ANSI).
        tast = cli.tastetrykk() # Detekterer tastetrykk
        if tast.lower() in cli.LUKK_TAST: # 'q', Esc, etc. er trykket
            return # Avslutter løkken for app og går tilbake til hovedløkke/hovedmeny
        
        elif tast == cli.TAST.ENTER: # Enter-tasten er trykket
            if not uttrykk:
                print("Uttrykket kan ikke være tomt.")
                continue

            print(f"\r> {uttrykk}")

            try:
                resultat = eval(uttrykk, {"__builtins__": None}, {})
                print(f"Svar: {resultat}")
            except Exception as e:
                print(f"Feil i uttrykket: {e}")
            
            # Ny utregning
            uttrykk = ""
            print("-" * (len(APPNAVN) + 8)) # Skilletegn for ny utregning
            print("Skriv inn nytt regnestykke:")
            continue

        elif tast in cli.TAST.BACKSPACE: # Backspace-tasten er trykket
            uttrykk = uttrykk[:-1] # Fjern siste tegn fra strengen

        else:
            if tast in "0123456789.+-*/() ": # Tillate verdier for matteuttrykk
                uttrykk += tast