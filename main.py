import query

def main():
    print("Benvenuto nel programma di localizzazione!")
    while True:
        print("\nScegli un'opzione:")
        print("1. Localizza una persona in una data e orario specifici")
        print("2. Trova i sospetti in una zona di reato")
        print("3. Trova le persone intestatarie delle SIM entro un raggio dalle coordinate geografiche")
        print("0. Esci")

        scelta = input("Inserisci il numero corrispondente all'opzione desiderata: ")

        if scelta == "1":
            print("\nScegli il tipo di ricerca:")
            print("1. Intervallo di date")
            print("2. Data e orario specifici")
            ricerca_scelta = input("Inserisci il numero corrispondente al tipo di ricerca desiderato: ")

            if ricerca_scelta == "1":
                data_inizio = input("Inserisci la data di inizio (formato YYYY-MM-DD): ")
                data_fine = input("Inserisci la data di fine (formato YYYY-MM-DD): ")
                persona = input("Inserisci il nome della persona: ")
                celle_telefoniche = query.localizza_persona(data_inizio, data_fine, persona)
                print("Le celle telefoniche collegate a", persona, "nell'intervallo di date specificato sono:", celle_telefoniche)

            elif ricerca_scelta == "2":
                data = input("Inserisci la data (formato YYYY-MM-DD): ")
                orario = input("Inserisci l'orario (formato HH:MM:SS): ")
                persona = input("Inserisci il nome della persona: ")
                celle_telefoniche = query.localizza_persona_ora(data, orario, persona)
                print("Le celle telefoniche collegate a", persona, "nella data e orario specificati sono:", celle_telefoniche)

            else:
                print("Scelta non valida. Riprova.")

        elif scelta == "2":
            data = input("Inserisci la data (formato YYYY-MM-DD): ")
            orario = input("Inserisci l'orario (formato HH:MM:SS): ")
            cella = input("Inserisci il nome della cella: ")
            sospetti = query.trova_sospetti(data, orario, cella)
            print("I sospetti nella zona di reato sono:", sospetti)

        elif scelta == "3":
            data = input("Inserisci la data (formato YYYY-MM-DD): ")
            orario = input("Inserisci l'orario (formato HH:MM:SS): ")
            latitudine = float(input("Inserisci la latitudine: "))
            longitudine = float(input("Inserisci la longitudine: "))
            raggio = float(input("Inserisci il raggio in metri: "))
            persone = query.trova_persone_in_raggio(latitudine, longitudine, raggio, data, orario)
            print("Le persone intestatarie delle SIM entro il raggio sono:")
            for sospetti, sim in persone:
                    print(f"{sospetti}, {sim}")

        elif scelta == "0":
            print("Grazie per aver utilizzato il programma di localizzazione. Arrivederci!")
            break

        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()

