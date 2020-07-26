import tkinter as tk
from functools import partial
import scrollable


def create_prelogin_screen(logo):
    menu = tk.Frame()

    def logowanie():
        set_frame(create_login_screen(img))

    def rejestracja():
        set_frame(create_registration_screen(img))

    menu.columnconfigure(1, weight=1, minsize=200)
    menu.columnconfigure(2, weight=1, minsize=200)
    menu.rowconfigure(1, weight=1, minsize=50)
    menu.rowconfigure(2, weight=1, minsize=50)
    menu.rowconfigure(3, weight=1, minsize=50)
    menu.rowconfigure(4, weight=1, minsize=15)

    # --------- 1 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=1, column=1, padx=40, pady=10, sticky="ew", columnspan=2)
    label1 = tk.Label(master=frame, image=logo)
    label1.pack()

    # --------- 2 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=2, column=1, padx=10, pady=10, sticky="n", columnspan=2)
    label1 = tk.Label(master=frame, text="Witaj! Co chcesz zrobić?", font=("Consolas", "15", 'bold'))
    label1.pack()

    # --------- 3 ROW ----------
    frame = tk.Frame(
        master=menu
    )
    frame.grid(row=3, column=1, padx=20, pady=10, sticky="e")
    button1 = tk.Button(master=frame, text="Logowanie", font=("Helvetica", "10", "bold"), command=logowanie)
    button1.pack()

    frame = tk.Frame(
        master=menu
    )
    frame.grid(row=3, column=2, padx=20, pady=10, sticky="w")
    button2 = tk.Button(master=frame, text="Rejestracja", font=("Helvetica", "10", "bold"), command=rejestracja)
    button2.pack()

    return menu


def create_login_screen(logo):
    menu = tk.Frame()

    def logowanie():
        set_frame(create_main_menu(img))

    def cofnij():
        set_frame(create_prelogin_screen(img))

    menu.columnconfigure(1, weight=1, minsize=100)
    menu.columnconfigure(2, weight=1, minsize=200)
    menu.columnconfigure(3, weight=1, minsize=100)
    menu.rowconfigure(1, weight=1, minsize=50)
    menu.rowconfigure(2, weight=1, minsize=50)
    menu.rowconfigure(3, weight=1, minsize=50)
    menu.rowconfigure(4, weight=1, minsize=50)
    menu.rowconfigure(5, weight=1, minsize=15)

    # --------- 1 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=1, column=1, padx=40, pady=10, sticky="ew", columnspan=3)
    label1 = tk.Label(master=frame, image=logo)
    label1.pack()

    frame = tk.Frame(
        master=menu
    )
    frame.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    button2 = tk.Button(master=frame, text="Cofnij", font=("Helvetica", "10"), command=cofnij)
    button2.pack()

    # --------- 2 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew", columnspan=3)
    entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry1.pack(side=tk.LEFT, expand=True)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=2, column=1, padx=10, pady=10, sticky="e")
    label1 = tk.Label(master=frame, text="Login", font=("Consolas", "10"))
    label1.pack()

    # --------- 3 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=3, column=1, padx=10, pady=10, sticky="ew", columnspan=3)
    entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry1.pack(side=tk.LEFT, expand=True)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=3, column=1, padx=10, pady=10, sticky="e")
    label1 = tk.Label(master=frame, text="Hasło", font=("Consolas", "10"))
    label1.pack()

    # --------- 4 ROW ----------
    frame = tk.Frame(
        master=menu
    )
    frame.grid(row=4, column=1, padx=20, pady=10, sticky="ew", columnspan=3)
    button1 = tk.Button(padx=64, master=frame, text="Zaloguj", font=("Helvetica", "10", "bold"), command=logowanie)
    button1.pack()

    return menu


def create_registration_screen(logo):
    menu = tk.Frame()

    def logowanie():
        set_frame(create_main_menu(img))

    def cofnij():
        set_frame(create_prelogin_screen(img))

    menu.columnconfigure(1, weight=1, minsize=100)
    menu.columnconfigure(2, weight=1, minsize=200)
    menu.columnconfigure(3, weight=1, minsize=100)
    menu.rowconfigure(1, weight=1, minsize=50)
    menu.rowconfigure(2, weight=1, minsize=50)
    menu.rowconfigure(3, weight=1, minsize=50)
    menu.rowconfigure(4, weight=1, minsize=50)
    menu.rowconfigure(5, weight=1, minsize=50)
    menu.rowconfigure(6, weight=1, minsize=50)
    menu.rowconfigure(7, weight=1, minsize=15)

    # --------- 1 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=1, column=1, padx=40, pady=10, sticky="ew", columnspan=3)
    label1 = tk.Label(master=frame, image=logo)
    label1.pack()

    frame = tk.Frame(
        master=menu
    )
    frame.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    button2 = tk.Button(master=frame, text="Cofnij", font=("Helvetica", "10"), command=cofnij)
    button2.pack()

    # --------- 2 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew", columnspan=3)
    entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry1.pack(side=tk.LEFT, expand=True)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=2, column=1, padx=10, pady=10, sticky="e")
    label1 = tk.Label(master=frame, text="Login", font=("Consolas", "10"))
    label1.pack()

    # --------- 3 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=3, column=1, padx=10, pady=10, sticky="ew", columnspan=3)
    entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry1.pack(side=tk.LEFT, expand=True)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=3, column=1, padx=10, pady=10, sticky="e")
    label1 = tk.Label(master=frame, text="Email", font=("Consolas", "10"))
    label1.pack()

    # --------- 4 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=4, column=1, padx=10, pady=10, sticky="ew", columnspan=3)
    entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry1.pack(side=tk.LEFT, expand=True)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=4, column=1, padx=10, pady=10, sticky="e")
    label1 = tk.Label(master=frame, text="Hasło", font=("Consolas", "10"))
    label1.pack()

    # --------- 5 ROW ----------
    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=5, column=1, padx=10, pady=10, sticky="ew", columnspan=3)
    entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry1.pack(side=tk.LEFT, expand=True)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=5, column=1, padx=10, pady=10, sticky="e")
    label1 = tk.Label(master=frame, text="Powtórz hasło", font=("Consolas", "10"))
    label1.pack()

    # --------- 6 ROW ----------
    frame = tk.Frame(
        master=menu
    )
    frame.grid(row=6, column=1, padx=20, pady=10, sticky="ew", columnspan=3)
    button1 = tk.Button(padx=54, master=frame, text="Zarejestruj", font=("Helvetica", "10", "bold"), command=logowanie)
    button1.pack()

    return menu


def create_main_menu(logo):
    menu = tk.Frame()
    def spis_polaczen():
        spis_pol = tk.Toplevel(menu)
        spis_pol.title("Spis połączeń - SecurCall")

        header = tk.Frame(spis_pol)
        header.pack()
        sp = tk.Frame(spis_pol)
        sp.pack()

        spis = scrollable.Scrollable(sp)

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
                },
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
                },
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
                },
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
                },
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
                },
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

        header.columnconfigure(1, weight=1, minsize=200)
        header.columnconfigure(2, weight=1, minsize=100)
        spis.columnconfigure(1, weight=1, minsize=200)
        spis.columnconfigure(2, weight=1, minsize=100)

        frame = tk.Frame(
            master=header,
        )
        frame.grid(row=1, column=1, padx=15, pady=10, columnspan=2)
        label = tk.Label(master=frame, text='Spis połączeń', font=("Consolas", "14", 'bold'))
        label.pack()

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

        spis.rowconfigure(rowcounter, weight=1, minsize=15)
        spis.update()


    # TODO wszystko tu xd
    def ustawienia():
        ustaw = tk.Toplevel(menu)
        ustaw.title("Ustawienia - SecurCall")

    # TODO notatka multiline
    def kontakty():
        def zadzwon_kontakt():
            pass

        def edytuj_kontakt(recnum):
            def zapisz_edycje():
                pass

            recnum -= 2
            edyt = tk.Toplevel(kontakt)
            edyt.title("Edycja kontaktu - SecurCall")

            edyt.columnconfigure(1, weight=1, minsize=50)
            edyt.columnconfigure(2, weight=1, minsize=200)
            edyt.rowconfigure(1, weight=1, minsize=50)
            edyt.rowconfigure(2, weight=1, minsize=50)
            edyt.rowconfigure(3, weight=1, minsize=50)
            edyt.rowconfigure(4, weight=1, minsize=50)
            edyt.rowconfigure(4, weight=1, minsize=50)


            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=1, column=1, padx=15, pady=10, sticky="w", columnspan=3)
            label1 = tk.Label(master=frame, text="Edycja kontaktu", font=("Consolas", "14", "bold"))
            label1.pack()

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=2, column=1, padx=10, pady=10, sticky="e", columnspan=2)
            entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
            entry1.insert(tk.END, testjs['dane'][recnum]['imie'])
            entry1.pack(side=tk.RIGHT, expand=True)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=2, column=1, padx=10, pady=10, sticky="e")
            label1 = tk.Label(master=frame, text="Nazwa", font=("Consolas", "10"))
            label1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=3, column=1, padx=10, pady=10, sticky="e", columnspan=2)
            entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
            entry1.insert(tk.END, testjs['dane'][recnum]['id'])
            entry1.pack(side=tk.RIGHT, expand=True)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=3, column=1, padx=10, pady=10, sticky="e")
            label1 = tk.Label(master=frame, text="ID", font=("Consolas", "10"))
            label1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=4, column=1, padx=10, pady=10, sticky="e", columnspan=2)
            text1 = tk.Text(master=frame, height=4, width=26, font=("Helvetica", "10"))
            text1.insert(tk.END, testjs['dane'][recnum]['notatka'])
            text1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=4, column=1, padx=10, pady=10, sticky="en")
            label1 = tk.Label(master=frame, text="Notatka", font=("Consolas", "10"))
            label1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt
            )
            frame.grid(row=1, column=2, padx=10, pady=10, sticky="e")
            button1 = tk.Button(master=frame, text="Zapisz", font=("Helvetica", "10", "bold"),
                                command=zapisz_edycje)
            button1.pack(side=tk.RIGHT)


        def usun_kontakt():
            pass

        kontakty = tk.Toplevel(menu)
        kontakty.title("Kontakty - SecurCall")

        header = tk.Frame(kontakty)
        header.pack()
        k = tk.Frame(kontakty)
        k.pack()

        kontakt = scrollable.Scrollable(k)

        testjs = {
            'dane': [
                {
                    'imie': 'Jan Kowalski',
                    'id': 'janekkk',
                    'notatka': 'Kierownik działu'
                },
                {
                    'imie': 'Robert Molenda',
                    'id': 'robert',
                    'notatka': ''
                },
                {
                    'imie': 'Jan Kowalski',
                    'id': 'janekkk',
                    'notatka': 'Kierownik działu'
                },
                {
                    'imie': 'Robert Molenda',
                    'id': 'robert',
                    'notatka': ''
                },
                {
                    'imie': 'Jan Kowalski',
                    'id': 'janekkk',
                    'notatka': 'Kierownik działu'
                },
                {
                    'imie': 'Robert Molenda',
                    'id': 'robert',
                    'notatka': ''
                },
                {
                    'imie': 'Jan Kowalski',
                    'id': 'janekkk',
                    'notatka': 'Kierownik działu'
                },
                {
                    'imie': 'Robert Molenda',
                    'id': 'robert',
                    'notatka': ''
                },
                {
                    'imie': 'Jan Kowalski',
                    'id': 'janekkk',
                    'notatka': 'Kierownik działu'
                },
                {
                    'imie': 'Robert Molenda',
                    'id': 'robert',
                    'notatka': ''
                },
                {
                    'imie': 'Jan Kowalski',
                    'id': 'janekkk',
                    'notatka': 'Kierownik działu'
                },
                {
                    'imie': 'Robert Molenda',
                    'id': 'robert',
                    'notatka': ''
                }
            ]
        }

        header.columnconfigure(1, weight=1, minsize=200)
        header.columnconfigure(2, weight=1, minsize=100)
        kontakt.columnconfigure(1, weight=1, minsize=200)
        kontakt.columnconfigure(2, weight=1, minsize=100)

        frame = tk.Frame(
            master=header,
        )
        frame.grid(row=1, column=1, padx=15, pady=10, columnspan=2)
        label = tk.Label(master=frame, text='Spis kontaktów', font=("Consolas", "14", 'bold'))
        label.pack()

        rowcounter = 2
        recordcounter = 0
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
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="e")
            button = tk.Button(master=frame, fg="green", text="Zadzwoń", font=("Helvetica", "10", "bold"),
                               command=partial(zadzwon_kontakt, recordcounter))
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
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="ne")
            button = tk.Button(master=frame, padx=11, text="Edytuj", font=("Helvetica", "10"),
                               command=partial(edytuj_kontakt, recordcounter))
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
            frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="ne")
            button = tk.Button(master=frame, padx=14.5, text="Usuń", font=("Helvetica", "10"), command=usun_kontakt)
            button.pack(side=tk.LEFT)
            buttons.append(button)

            rowcounter += 1
            recordcounter += 1

        kontakt.rowconfigure(rowcounter, weight=1, minsize=15)
        kontakt.update()


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


def set_frame(new_frame):
    global current

    # hide current tk.Frame
    current.pack_forget()

    # show new tk.Frame
    current = new_frame
    current.pack()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("SecurCall")

    global img
    img = tk.PhotoImage(file="logo.png")
    img = img.subsample(1, 1)

    current = create_prelogin_screen(img)
    current.pack()
    #set_frame(create_main_menu(img))
    root.mainloop()

