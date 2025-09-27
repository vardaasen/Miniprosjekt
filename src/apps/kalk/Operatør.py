# Operatørfunksjoner
'''
Operatør modulen: Inneholder matematiske funksjoner brukt i kalkulatoren (appen).

Jeg har valgt å lage egne funksjoner for hver operasjon (pluss, minus, gange, dele, prosentregning).
Dette gir koden en modulær struktur som er:
- Fleksibel: lett å endre uten å påvirke andre deler av programmet.
- Testbar: hver funksjon kan testes isolert.
- Gjenbrukbar: kan importeres i andre prosjekter.
- Utvidbar: nye operasjoner kan enkelt legges til.
- Oversiktlig: koden blir lettere å lese og forstå i større systemer.

Kilder brukt til læring og inspirasjon:
- W3Schools: https://www.w3schools.com/python/python_operators.asp
- GeeksforGeeks: https://www.geeksforgeeks.org/python/python-operators/
- Copilot: brukt som veiledning for struktur og feilmeldinger.
- Egne erfaring fra tidligere.

Jeg skriver koden selv og tester underveis. Når jeg møter feil, bruker jeg kilder og Copilot
for å få tips og forstå hvorfor feilen oppstår. På denne måten bygger jeg faktisk forståelse.
'''


'''
    Returnerer summen av to tall.
    Parametre:
        x (float/int): første tall
        y (float/int): andre tall
    Return:
        float/int: summen av x og y
    '''


def mike_plus(x, y):  # Funksjonen mike_plus som inneholder hva den skal gjøres, når funksjonen blir kalt.
  return x + y  # Return sender resultatet (summen) tilbake til stedet funksjonen ble kalt fra, eksemple 
                #  return Op.plus(num1_input, num2_input) i fra Valg.py.


def mike_minus(x, y):   
    return x - y  

'''
Når du lager en funksjon, bestemmer du navnene på tallene som skal brukes inne i funksjonen. 
Disse navnene kalles parametere.Hvis du velger a og b, må du også bruke a og b når du regner i return. 
Hvis du skriver noe annet (som x og y), skjønner ikke Python hva du mener og gir en feil.
'''


def mike_gange(x, y):
    return x * y


def mike_dele(x, y):
    if y == 0:
        return "Error: Kan ikke dele med tallet 0"
    return x / y

"""
    Deler x med y, med sikkerhetssjekk for y == 0 for å unngå ZeroDivisionError.
    I Python vil uttrykket 'x / 0' gi en ZeroDivisionError (kilde. GeeksforGeeks:
    https://www.geeksforgeeks.org/python/zerodivisionerror-integer-by-zero-in-python/ 
    https://www.geeksforgeeks.org/python/zerodivisionerror-float-division-by-zero-in-python/
    https://www.geeksforgeeks.org/python/python-exception-handling/
    Hvis y == 0, returnerer vi en brukervennlig feilmelding i stedet for at programmet krasjer.
"""
  


'''
Funksjonen for prosentregning beregner hvor mange prosent et tall utgjør av et annet.
Formelen er: (x / 100) * y, der x er prosentandelen og y er grunnlaget.

For å presentere resultatet på en ryddig måte brukes en f-streng:
f"{x}% av {y} er {total:.2f}"

- x og y settes inn direkte i teksten slik at brukeren får en forståelig utskrift.
- total formateres med `:.2f`, som betyr at tallet vises med to desimaler.
  Dette gjør svaret mer presist og ser mer profesjonelt ut.

Ved å kombinere selve beregningen og utskriften i én funksjon,
blir koden både enkel å lese og lett å gjenbruke i andre sammenhenger.
'''


'''
    Beregner hvor mange prosent x utgjør av y.
    Eksempel: prosentregn(13, 287) -> '13% av 287 er 37.31'
    Resultatet formateres med to desimaler for å se ryddig ut, ved å bruke .2f
'''

def mike_prosentregn(x, y):
    total = (x / 100) * y
    return f"{x}% av {y} er {total:.2f}"



'''
Refleksjon:
Jeg har holdt meg til et nivå jeg faktisk har kunnskap om og forståelse for.
Man lærer ikke noe av å kopiere eller lyve til seg selv, derfor har jeg
skrevet koden selv, men brukt kildene over som støtte til læring og utvikling.
'''