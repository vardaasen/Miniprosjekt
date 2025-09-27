APPNAVN = "TODO-liste | Chinh"

todo = []

def app():
    while True:
        print("\n--- To-do-liste ---")
        print("1. Legg til oppgave")
        print("2. Vis alle oppgaver")
        print("3. Slett oppgave")
        print("4. Avslutt")

        valg = input("Velg en funksjon (1-4)")

        if valg == "1":
            oppgave = input("Skriv inn en oppgave: ")
            todo.append(oppgave)
            print("Oppgave lagt til.")
            

        elif valg == "2":
            if todo:
                print("Oppgaver:")
                for i, oppgave in enumerate(todo, start=1):
                    print(f"{i}. {oppgave}")

            else:
                print("Ingen oppgaver enda.")

        elif valg == "3":
                if todo:
                    for i, oppgave in enumerate(todo, start=1):
                        print(f"{i}. {oppgave}")
                    slett = int(input("Hvilket nr vil du slette")) - 1
                    if 0 <= slett < len(todo):
                        fjernet = todo.pop(slett)
                        print(f"Oppgave '{fjernet}' slettet.")
                    else:
                        print("Ugyldig nummer.")
                else:
                    print("Ingen oppgaver å slette.")

        elif valg == "4":
                print("Avslutt to-do-listen...")
                break

        else:
                print("Ugyldig valg. Prøv igjen.")
if __name__ == "__main__":
# Start to-do listen
    app()