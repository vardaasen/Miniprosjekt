# Hovedfilen for kalkulator appen.
# Her definerer vi appens navn og selve startfunksjonen "app()".
# Denne brukes av hovedprogrammet til å starte kalkulatoren når brukeren velger den i menyen.

APPNAVN = "Kalkulator | Michael"   # Navnet som vises i hovedmenyen i Hovedprogram.py.

from . import Valg       # Importerer Valg-modulen som håndterer menyvalg og input/output.

# app() fungerer som "nøkkel" til denne appen, for å hente eller starte fra hovedmenyen. 
# Hovedprogrammet kaller alltid på app() når brukeren har valgt kalkulatoren. Det er definert i hvoedmenyen at det må gis navn som app().
# Derfor må alle apper i prosjektet ha både APPNAVN og en app()  funksjon.
def app():
    while True:  # Kjører i en løkke slik at brukeren kan utføre flere beregninger før han avslutter med "avslutt" eller "exist".
        Valg.mike_valg()  # Viser kalkulatorens  meny
        valg_input = input("Velg funksjon: ").strip().lower()  # Tar imot brukerens valg.

        # Hvis brukeren vil avslutte kalkulatoren
        if valg_input in ("exit", "avslutt"):
            print("Avslutter programmet...")
            break # break gjør at while True løkka i app() stoppes -> altså kalkulator appen avsluttes.

        # Hvis brukeren velger hurtig kalkulering (pluss, minus, gange, dele).
        if valg_input == "1":
            print("Resultat:", Valg.mike_kakulering()) # Hvis valget er "1" vil kalkulator funksjonen starte. 

        # Hvis brukeren velger prosentregning.
        elif valg_input == "2":
            print(Valg.mike_prosent()) # Her kalles eller hentes funksjonen fra "Valg" "print" er som å pakke ut, pakken du har motatt.

        # Hvis brukeren skriver inn noe ugyldig. 
        else:
            print("Ugyldig valg, prøv igjen.")

# Denne sjekken gjør at kalkulatoren kan startes både direkte (python Start.py).
# og via hovedprogrammet.
if __name__ == "__main__":
    app() # denne gjør at min appen kan også starte, individuelt uavhengig av hovedprogrammet. 




'''
Start modulen: 

Kilder jeg har brukt for inspirasjon og læring:
- W3Schools: https://www.w3schools.com/python/python_functions.asp (funksjoner)
- GeeksforGeeks: https://www.geeksforgeeks.org/python/while-loop/ (while-løkker)
- Python docs: https://docs.python.org/3/tutorial/controlflow.html (kontrollstrukturer)
- Copilot: brukt som veiledning for struktur og feilhåndtering
Refleksjon:
Jeg har holdt meg til et nivå jeg faktisk har kunnskap om og forståelse for.
Man lærer ikke noe av å kopiere eller lyve til seg selv, derfor har jeg
skrevet koden selv, men brukt kildene over som støtte til læring og utvikling.
'''

