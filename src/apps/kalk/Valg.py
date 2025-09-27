from . import Operatør as Op    # Importerer Operatør modulen og gir den kortnavnet "Op".
                                # Nå kan vi bruke Op.plus(), Op.minus() osv. i stedet for å skrive Operatør.plus().
                                # Trenger ikke å endre linje fremover, dersom jeg legger inn flere funksjoner i Operatør. 

def mike_valg(): # Definerer funksjonen meny_valg() som kan kalles fra annen file/program senere. 
    print("\nVelkommen til hurtig kalkulator")
    #  meny_liste som inneholder informasjon og valg brukeren kan velge mellom. 
    meny_liste = [
        "Skriv 'avslutt' eller 'exit' for å avslutte programmet", # Informere om hvordan brukere kan avslutte programmet. 
        "Tast 1 for hurtig kalkulering (+, -, /, *)", # Viser brukeren at de kan velge mellom enkelt regning eller prosent %.
        "Tast 2 for prosentregning (eks: 13% av 287)"
    ]
    for liste in meny_liste: # Går gjennom hvert element i meny_liste og skriver det ut.
        print(liste) # Skriver ut ett menyvalg per linje.


def mike_kakulering():   # Funksjonen for vanlig regning (pluss, minus, gange, dele), som skal fremmkalles fra Start.py.
    try:   # Starter en try blokk for å fange opp feil hvis brukeren skriver ugyldig input.
        num1_input = float(input("Skriv inn første tall: "))   # Leser første tallet fra brukeren og konverterer til float.
        operatør = input("Velg en operatør (+,-,/,*): ").strip()   # Leser inn valgt operator og fjerner mellomrom med strip().
        num2_input = float(input("Skriv inn andre tallet: "))   # Leser andre tallet fra brukeren og konverterer til float.
    except ValueError:   # Hvis input ikke kan gjøres om til tall (f.eks. bokstaver), fanges feilen her.
        return "Ugyldig tall, prøv igjen."   # Returnerer feilmelding til brukeren.

    if operatør == "+":   # Hvis brukeren valgte pluss.
        return Op.mike_plus(num1_input, num2_input)   # Kaller funksjonen plus() fra Operatør og returnerer summen.
    elif operatør == "-":   # Hvis brukeren valgte minus.
        return Op.mike_minus(num1_input, num2_input)   # Kaller minus() og returnerer differansen.
    elif operatør == "*":   # Hvis brukeren valgte gange.
        return Op.mike_gange(num1_input, num2_input)   # Kaller gange() og returnerer produktet.
    elif operatør == "/":   # Hvis brukeren valgte dele.
        return Op.mike_dele(num1_input, num2_input)   # Kaller dele() og returnerer kvotienten (eller feilmelding hvis /0).
    else:   # Hvis brukeren skrev inn noe annet enn + - * /.
        return "Ugyldig operatør"   # Returnerer feilmelding til brukeren.

def mike_prosent():   # Funksjonen for prosentregning, som kalles senere fra Start.py
    try:   # Starter en try blokk for å fange opp ugyldige tall.
        prosent_kalk = float(input("Skriv prosent (eks. 13 for 13%): "))   # Leser inn prosentverdien og konverterer til float.
        total = float(input("Skriv tallet du vil finne prosent av: "))   # Leser inn tallet man skal regne prosent av.
    except ValueError:   # Hvis brukeren skrev ugyldige tall (bokstaver eller annet enn definert tegn).
        return "Ugyldig tall, prøv igjen."   # Returnerer feilmelding.
    return Op.mike_prosentregn(prosent_kalk, total)   # Kaller prosentregn() i Operatør for å utføre selve beregningen.

'''
Kilder og inspirasjon:
Jeg har brukt tidligere kunnskaper og øvd selv, men hentet støtte og eksempler fra
følgende kilder:

- W3Schools (grunnleggende Python eksempler og forklaringer):
  https://www.w3schools.com/python/python_while_loops.asp
  https://www.w3schools.com/python/python_conditions.asp

- GeeksforGeeks (mer detaljerte artikler og forklaringer):
  https://www.geeksforgeeks.org/python/loops-in-python/
  https://www.geeksforgeeks.org/python/python-functions/
  https://www.geeksforgeeks.org/python/conditional-statements-in-python/
  https://www.geeksforgeeks.org/python/python-exception-handling/

- Offisiell Python-dokumentasjon (kontrollstrukturer og moduler):
  https://docs.python.org/3/tutorial/

- Copilot (brukt som veiledning for struktur, feilmeldinger og forslag).
  Jeg har skrevet koden selv og testet underveis. Når jeg satt fast,
  brukte jeg Copilot for å forstå feil og få tips til løsninger.

Refleksjon:
Jeg har holdt meg til et nivå jeg faktisk har kunnskap om og forståelse for.
Man lærer ikke noe av å kopiere eller lyve til seg selv, derfor har jeg
skrevet koden selv, men brukt kildene over som støtte til læring og utvikling.
'''
