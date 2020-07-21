import tkinter as tk


def create_main_menu(menu, logo):
    # TODO stała wielkość okna przy dużej liczbie rekordów
    def spis_polaczen():
        spis = tk.Toplevel(menu)
        spis.title("Spis połączeń - SecurCall")

        testjs = {
            'dane': [
                {
                    'imie': 'Jan Kowalski',
                    'czas_rozmowy': '45:21',
                    'data': '10.04.2020',
                    'godzina': '12:05'
                },
                {
                    'imie': 'Robert Molenda',
                    'czas_rozmowy': '1:21',
                    'data': '21.04.2020',
                    'godzina': '3:05'
                }
            ]
        }

        spis.columnconfigure(1, weight=1, minsize=200)
        spis.columnconfigure(2, weight=1, minsize=100)

        frame = tk.Frame(
            master=spis,
        )
        frame.grid(row=1, column=1, padx=15, pady=10, sticky="nw", columnspan=2)
        label = tk.Label(master=frame, text='Spis połączeń', font=("Consolas", "14", 'bold'))
        label.pack(side=tk.LEFT)

        rowcounter = 2

        for record in testjs['dane']:
            frame = tk.Frame(
                master=spis,
            )
            frame.grid(row=rowcounter, column=1, padx=15, pady=3, sticky="w")
            label = tk.Label(master=frame, text=record['imie'], font=("Consolas", "11", 'bold'))
            label.pack(side=tk.LEFT)

            frame = tk.Frame(
                master=spis,
            )
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="e")
            label = tk.Label(master=frame, text=record['data'], font=("Helvetica", "10"))
            label.pack(side=tk.RIGHT)

            rowcounter += 1

            frame = tk.Frame(
                master=spis,
            )
            frame.grid(row=rowcounter, column=1, padx=15, pady=3, sticky="w")
            label = tk.Label(master=frame, text='Czas rozmowy: ' + record['czas_rozmowy'], font=("Helvetica", "10"))
            label.pack(side=tk.LEFT)

            frame = tk.Frame(
                master=spis,
            )
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="e")
            label = tk.Label(master=frame, text=record['godzina'], font=("Helvetica", "10"))
            label.pack(side=tk.RIGHT)

            rowcounter += 1

    # TODO wszystko tu xd
    def ustawienia():
        ustaw = tk.Toplevel(menu)
        ustaw.title("Ustawienia - SecurCall")

    # TODO stała wielkość okna przy dużej liczbie rekordów, notatka multiline
    def kontakty():
        def zadzwon_kontakt():
            pass

        def edytuj_kontakt():
            pass

        def usun_kontakt():
            pass

        kontakt = tk.Toplevel(menu)
        kontakt.title("Kontakty - SecurCall")
        testjs = {
            'dane': [
                {
                    'imie': 'Jan Kowalski',
                    'id': 'janekkk',
                    'notatka': 'Kierownik działu blablalbalbalblablalbalblalbladbadlbaldbl asfasfassa fasfasf'
                },
                {
                    'imie': 'Robert Molenda',
                    'id': 'robert',
                    'notatka': ''
                }
            ]
        }

        kontakt.columnconfigure(1, weight=1, minsize=200)
        kontakt.columnconfigure(2, weight=1, minsize=100)

        frame = tk.Frame(
            master=kontakt,
        )
        frame.grid(row=1, column=1, padx=15, pady=10, sticky="nw", columnspan=2)
        label = tk.Label(master=frame, text='Spis kontaktów', font=("Consolas", "14", 'bold'))
        label.pack(side=tk.LEFT)

        rowcounter = 2
        labels = []
        buttons = []
        for record in testjs['dane']:
            frame = tk.Frame(
                master=kontakt,
            )
            frame.grid(row=rowcounter, column=1, padx=15, pady=10, sticky="nw")
            label = tk.Label(master=frame, text=record['imie'], font=("Consolas", "11", 'bold'))
            label.pack(side=tk.LEFT)
            labels.append(label)

            frame = tk.Frame(
                master=kontakt,
            )
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="s")
            button = tk.Button(master=frame, fg="green", text="Zadzwoń", font=("Helvetica", "10", "bold"),
                               command=zadzwon_kontakt)
            button.pack(side=tk.LEFT)
            buttons.append(button)

            rowcounter += 1

            frame = tk.Frame(
                master=kontakt,
            )
            frame.grid(row=rowcounter, column=1, padx=15, pady=3, sticky="nw")
            label = tk.Label(master=frame, text='ID: ' + record['id'], font=("Helvetica", "10"))
            label.pack(side=tk.LEFT)
            labels.append(label)

            frame = tk.Frame(
                master=kontakt,
            )
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="nw")
            button = tk.Button(master=frame, padx=11, text="Edytuj", font=("Helvetica", "10"), command=edytuj_kontakt)
            button.pack(side=tk.LEFT)
            buttons.append(button)

            rowcounter += 1

            frame = tk.Frame(
                master=kontakt,
            )
            frame.grid(row=rowcounter, column=1, padx=15, pady=3, sticky="nw")
            if record['notatka'] == '':
                label = tk.Label(master=frame, text='Brak notatki.', font=("Helvetica", "10"))
                label.pack(side=tk.LEFT)
                labels.append(label)
            else:
                label = tk.Label(master=frame, text=record['notatka'], font=("Helvetica", "10"))
                label.pack(side=tk.LEFT)
                labels.append(label)

            frame = tk.Frame(
                master=kontakt,
            )
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="nw")
            button = tk.Button(master=frame, padx=14.4, text="Usuń", font=("Helvetica", "10"), command=usun_kontakt)
            button.pack(side=tk.LEFT)
            buttons.append(button)

            rowcounter += 1

    def zadzwon():
        entry1.insert(0, 'kliknieto')

    def rozlacz():
        pass

    def wylacz_mikrofon():
        pass

    def wycisz_dzwiek():
        pass

    menu.columnconfigure(1, weight=1, minsize=70)
    menu.columnconfigure(2, weight=1, minsize=150)
    menu.columnconfigure(3, weight=1, minsize=70)
    menu.rowconfigure(1, weight=1, minsize=50)
    menu.rowconfigure(2, weight=1, minsize=50)
    menu.rowconfigure(3, weight=1, minsize=40)
    menu.rowconfigure(4, weight=1, minsize=50)

    # --------- 1 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=1, column=1, padx=15, pady=10, sticky="w", columnspan=2)
    label1 = tk.Label(master=frame, image=logo)
    label1.pack()

    frame = tk.Frame(
        master=menu,
        borderwidth=1
    )
    frame.grid(row=1, column=2, pady=10, sticky="e", columnspan=2)
    button1 = tk.Button(master=frame, text="Spis połączeń", font=("Helvetica", "10"), command=spis_polaczen)
    button1.pack(side=tk.RIGHT, padx=10)
    button2 = tk.Button(master=frame, text="Ustawienia", font=("Helvetica", "10"), command=ustawienia)
    button2.pack()

    frame = tk.Frame(
        master=menu,
        borderwidth=1
    )
    frame.grid(row=1, column=3, padx=10, pady=15)

    # --------- 2 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=2, column=1, padx=15, pady=10, sticky="w")
    button3 = tk.Button(master=frame, text="Kontakty", font=("Helvetica", "10"), command=kontakty)
    button3.pack()

    frame = tk.Frame(
        master=menu,
        borderwidth=1,
    )
    frame.grid(row=2, column=2, pady=10, sticky="e")
    entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry1.insert(tk.END, 'ID użytkownika')
    entry1.pack(side=tk.LEFT, expand=True)
    button4 = tk.Button(master=frame, text=" + ", font=("Helvetica", "8", 'bold'))
    button4.pack(side=tk.RIGHT)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=2, column=2, pady=0, sticky="n")
    error_label = tk.Label(master=frame, text="", font=("Helvetica", "8"), fg='red')
    error_label.pack()

    frame = tk.Frame(
        master=menu,
        borderwidth=1
    )
    frame.grid(row=2, column=3, padx=10, pady=10)
    button5 = tk.Button(master=frame, fg="green", text="Zadzwoń", font=("Helvetica", "10", "bold"), command=zadzwon)
    button5.pack()

    # --------- 3 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=3, column=1, padx=15, sticky="w", columnspan=2)
    label2 = tk.Label(master=frame, text="Aktualnie rozmawiasz z:", font=("Helvetica", "8"))
    label2.pack()

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=3, column=2, padx=15, sticky="e", columnspan=2)
    label3 = tk.Label(master=frame, text="Notatka o rozmówcy:", font=("Helvetica", "8"))
    label3.pack()

    # --------- 4 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=4, column=1, padx=15, pady=0, sticky="w", columnspan=2)
    label4 = tk.Label(master=frame, text="Jan Kowalski", font=("Consolas", "10", "bold"))
    label4.pack(side=tk.TOP, pady=3)
    button6 = tk.Button(master=frame, padx=20, fg="red", text="Rozłącz", font=("Helvetica", "10", "bold"), command=rozlacz)
    button6.pack(side=tk.BOTTOM, pady=10)

    frame = tk.Frame(
        master=menu,
        borderwidth=1
    )
    frame.grid(row=4, column=2, padx=15, pady=0)
    button7 = tk.Button(master=frame, text="Wyłącz mikrofon", font=("Helvetica", "10"), command=wylacz_mikrofon)
    button7.pack(side=tk.TOP)
    button8 = tk.Button(master=frame, padx=6, text="Wycisz dźwięk", font=("Helvetica", "10"), command=wycisz_dzwiek)
    button8.pack(side=tk.BOTTOM, pady=10)

    frame = tk.Frame(
        master=menu,
        borderwidth=1
    )
    frame.grid(row=4, column=2, padx=15, pady=0, columnspan=2, sticky="ne")
    text1 = tk.Text(master=frame, height=4, width=15, font=("Helvetica", "10"))
    text1.pack(side=tk.TOP)
    return menu


if __name__ == '__main__':
    men = tk.Tk()
    men.title("SecurCall")

    img = tk.PhotoImage(file="logo.png")
    img = img.subsample(1, 1)

    men = create_main_menu(men, img)
    men.mainloop()

