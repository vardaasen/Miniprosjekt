from utils import cli
from random import randint
from base64 import b64decode, b64encode

APPNAVN = "Sikkerhetsverktøy | Kristoffer"

def passordgenerator():
    """
    Passordgenerator som tar brukerinput og genererer et sterkt passord med ALLE utsrivbare tegn som deretter vises i terminalen.
    Metoden for å generere passordet bruker `randint(33, 126)` for å lage et tilfeldig heltall som deretter konverteres til et tegn med chr().
    Tallrekken (33-126) i randint representerer alle de utskrivbare tegnene i standard ASCII-tabellen.
    For å overskrive forrige passord i terminalen benyttes ANSI escape-sekvenser.
    """
    TITTEL = "Passordgenerator"
    cli.cls()
    print(f"--- {TITTEL} ---")
    print("Trykk Enter for å generere et sterkt passord på 20 tegn.")
    print("\n" + cli.LUKK_STR)
    print("-" * (len(TITTEL) + 8))
    passord_printet = False
    while True:
        tast = cli.tastetrykk()  # Venter på tastetrykk
        if tast.lower() in cli.LUKK_TAST: # 'q', Esc, etc. er trykket
            return # Avslutter løkken for app og går tilbake til undermeny
        if tast == cli.TAST.ENTER:
            passord = ""
            for _ in range(20): # Vi kjører løkken 20 ganger for passord på 20 tegn
                tilfeldig_tall = randint(33, 126) # Genererer tilfeldig heltall mellom 33 og 126 som representerer ALLE utskrivbare tegn fra ASCII-tabellen (kjent som ASCII-94)
                tilfeldig_tegn = chr(tilfeldig_tall) # chr() konverterer tallet til tegn fra ASCII-tabellen
                passord += tilfeldig_tegn
            # Logikk for å kunne overskrive forrige passord ved hjelp av Escape-sekvens '\033[1A' (flytt markør opp en linje) og '\r' (til start av linje)
            # Hvis man skal flytte opp to linjer må man bruke '\033[2A', osv. hvor [2A betyr "flytt opp to linjer" (som jeg måtte gjort uten end='' i print)
            print(f"{'\033[1A\r' if passord_printet else ''}Sterkt passord (trykk Enter for nytt passord):\n{passord}", end='')
            passord_printet = True # Flagg for å sjekke om passord er printet før

def xor_krypter(data, nøkkel):
    """
    Krypterer eller dekrypterer data ved hjelp av XOR-operasjon.

    Funksjonen er reversibel ettersom data tilbakestilles ved å utføre XOR-operasjonen to ganger: (data ^ nøkkel) ^ nøkkel = data.
    Input: data (bytes), nøkkel (bytes)
    Output: kryptert eller dekryptert data (bytes)

    Koden er skrevet selv, men har benyttet ressurser på nett 

    Kilder:
    XOR chifferering: https://en.wikipedia.org/wiki/XOR_cipher
    Bytearray og bytes: https://realpython.com/python-bytearray/
    """
    resultat = bytearray()
    nøkkel_lengde = len(nøkkel)
    for i in range(len(data)): # Vi itererer over hver byte i 'data' og gjør en XOR-operasjon på data ^ nøkkel, byte for byte
        xor_verdi = data[i] ^ nøkkel[i % nøkkel_lengde] # Vi bruker % (modulus) for å gjenta nøkkel hvis den er kortere enn data
        resultat.append(xor_verdi) # Vi legger til XOR verdien i en bytearray (samling)
    return bytes(resultat) # Bytearray endres til et bytes object likt det som kom inn i data

def krypteringsverktøy():
    """
    Wrapper-funksjon som tar brukerinput, krypterer/dekrypterer med xor_krypter, og formaterer melding basert på en hemmelig nøkkel som printes til terminalen.
    """
    TITTEL = "Krypteringsverktøy"
    cli.cls()
    print(f"--- {TITTEL} ---")
    print("Krypter og dekrypter en melding ved hjelp av en hemmelig nøkkel.")
    print("\n" + cli.LUKK_STR)
    print("-" * (len(TITTEL) + 8))

    while True:
        # Validering for å sjekke at input ikke er tom
        while not (melding := input("Tast inn melding: ")):
            print("\033[1A\rMelding er tom, prøv på nytt... ", end='')
        print(f"\033[1A{' '*(len(melding)+50)}\r", end='') # Overskriver forrige linje i terminalen med ASCII Escape-sekvenser
        while not (nøkkel := input("Tast inn nøkkel: ")):
            print(f"\033[1A\rNøkkel er tom, prøv på nytt... ", end='')
        print(f"\033[1A{' '*(len(nøkkel)+50)}\r", end='')
        print("Melding før kryptering:", melding)
        print("Trykk en tast for å kryptere meldingen...")
        tast = cli.tastetrykk()
        if tast.lower() in cli.LUKK_TAST:
            return
        print(f"\033[1A{' '*50}\r", end='') # Overskriver forrige linje i terminalen
        # Melding og nøkkel gjøres om til bytes for XOR-operasjon
        melding_bytes = melding.encode('utf-8')
        nøkkel_bytes = nøkkel.encode('utf-8')
        # Data krypteres og gjøres til en Base64-streng som bedre for eksportering og for å vises i terminalen
        kryptert_bytes = xor_krypter(melding_bytes, nøkkel_bytes)
        kryptert_lesbar = b64encode(kryptert_bytes).decode('utf-8')
        print(f"Melding etter kryptering: {kryptert_lesbar}")
        
        print("Trykk en tast for å dekryptere meldingen...")
        tast = cli.tastetrykk()
        if tast.lower() in cli.LUKK_TAST:
            return
        print(f"\033[1A{' '*50}\r", end='') # Overskriver forrige linje i terminalen
        # Dekryptering og print av meldingen
        dekryptert_bytes = xor_krypter(b64decode(kryptert_lesbar), nøkkel_bytes) # Base64-strengen konverteres tilbake til bytes før dekryptering
        dekryptert_melding = dekryptert_bytes.decode('utf-8') # Dekrypterte bytes dekodes tilkake Unicode UTF-8 tekstreng (reversert fra 'original').
        print(f"Melding etter dekryptering: {dekryptert_melding}")
        print(f"\nDekryptert melding er lik som opprinnelig melding: {'SANT' if dekryptert_melding == melding else 'USANT'}")
        print("Trykk en tast for å gå tilbake...")
        cli.tastetrykk()
        return

APPVALG = { # Menyliste med tastevalg og tilhørende funksjon som skal kjøres
    '1': passordgenerator,
    '2': krypteringsverktøy
}

def vis_meny():
    print(f"--- {APPNAVN} ---")
    print("Velg program fra undermeny:")
    print(" 1. Passordgenerator")
    print(" 2. Krypteringsverktøy")
    print("\n" + cli.LUKK_STR)
    print("-" * (len(APPNAVN) + 8))

def app():
    cli.cls()
    vis_meny()

    while True:
        tast = cli.tastetrykk()
        if tast.lower() in cli.LUKK_TAST:
            return
        elif tast in APPVALG:
            APPVALG[tast]() # Kjør valgt funksjon

            # Tøm terminal og vis undermeny på nytt når funksjon er avsluttet
            cli.cls()
            vis_meny()

"""
Koden er skrevet selv, men har benyttet følgende kilder og nettressurser for oppslag og veiledning.

Kilder:
ASCII tabell og utskrivbare tegn: https://www.ascii-code.com/

Base64: https://www.geeksforgeeks.org/python/encoding-and-decoding-base64-strings-in-python/
Walrus operator (:=): https://realpython.com/python-walrus-operator/


"""
