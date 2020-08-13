import pprint
import threading
import tkinter as tk
from functools import partial
import scrollable
import time
import client


c = client.Client(
    server_addr='127.0.0.1',
    server_port=1337,
)


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


def create_login_screen(logo, errortext=''):
    menu = tk.Frame()

    def logowanie():
        res = c.log_in(entry1.get(), entry2.get())
        if res is True:
            set_frame(1, True)
        else:
            errorlabel['text'] = 'Błędne dane!'

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
    label1.pack(side=tk.TOP)
    errorlabel = tk.Label(master=frame, text=errortext, font=("Helvetica", "10", "bold"), fg="red")
    errorlabel.pack(side=tk.BOTTOM)

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
    entry2 = tk.Entry(master=frame, show="*", font=("Helvetica", "13"))
    entry2.pack(side=tk.LEFT, expand=True)

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
        if entry3.get() == entry4.get():
            res = c.sign_in(entry1.get(), entry3.get(), entry2.get())
            if res is True:
                # set_frame(create_registration_screen(img))
                set_frame(create_login_screen(img, 'Pomyślnie zarejestrowano! Możesz się zalogować :)'))
            else:
                errorlabel['text'] = 'Błędne dane!'

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
    errorlabel = tk.Label(master=frame, text="", font=("Helvetica", "10", "bold"), fg="red")
    errorlabel.pack(side=tk.BOTTOM)

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
    entry2 = tk.Entry(master=frame, font=("Helvetica", "13"))
    entry2.pack(side=tk.LEFT, expand=True)

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
    entry3 = tk.Entry(master=frame, show="*", font=("Helvetica", "13"))
    entry3.pack(side=tk.LEFT, expand=True)

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
    entry4 = tk.Entry(master=frame, show="*", font=("Helvetica", "13"))
    entry4.pack(side=tk.LEFT, expand=True)

    frame = tk.Frame(
        master=menu,
    )
    frame.grid(row=5, column=1, padx=10, pady=10, sticky="e")
    label4 = tk.Label(master=frame, text="Powtórz hasło", font=("Consolas", "10"))
    label4.pack()

    # --------- 6 ROW ----------
    frame = tk.Frame(
        master=menu
    )
    frame.grid(row=6, column=1, padx=20, pady=10, sticky="ew", columnspan=3)
    button1 = tk.Button(padx=54, master=frame, text="Zarejestruj", font=("Helvetica", "10", "bold"), command=logowanie)
    button1.pack()

    return menu


class main_menu:
    def __init__(self, master, logo):
        self.master = master
        self.menu = tk.Frame()

        self.menu.columnconfigure(1, weight=1, minsize=70)
        self.menu.columnconfigure(2, weight=1, minsize=150)
        self.menu.columnconfigure(3, weight=1, minsize=70)
        self.menu.rowconfigure(1, weight=1, minsize=50)
        self.menu.rowconfigure(2, weight=1, minsize=50)
        self.menu.rowconfigure(3, weight=1, minsize=40)
        self.menu.rowconfigure(4, weight=1, minsize=50)

        # --------- 1 ROW ----------
        frame = tk.Frame(
            master=self.menu,
        )
        frame.grid(row=1, column=1, padx=15, pady=10, sticky="w", columnspan=2)
        self.label1 = tk.Label(master=frame, image=logo)
        self.label1.pack()

        frame = tk.Frame(
            master=self.menu,
            borderwidth=1
        )
        frame.grid(row=1, column=2, pady=10, sticky="e", columnspan=2)
        self.button1 = tk.Button(master=frame, text="Spis połączeń", font=("Helvetica", "10"), command=self.spis_polaczen)
        self.button1.pack(side=tk.RIGHT, padx=10)
        self.button2 = tk.Button(master=frame, text="Ustawienia", font=("Helvetica", "10"), command=self.ustawienia)
        self.button2.pack()

        frame = tk.Frame(
            master=self.menu,
            borderwidth=1
        )
        frame.grid(row=1, column=3, padx=10, pady=15)

        # --------- 2 ROW ----------
        frame = tk.Frame(
            master=self.menu,
        )
        frame.grid(row=2, column=1, padx=15, pady=10, sticky="w")
        self.button3 = tk.Button(master=frame, text="Kontakty", font=("Helvetica", "10"), command=self.kontakty)
        self.button3.pack()

        frame = tk.Frame(
            master=self.menu,
            borderwidth=1,
        )
        frame.grid(row=2, column=2, pady=10, sticky="e")
        self.sv = tk.StringVar()
        self.entry1 = tk.Entry(master=frame, font=("Helvetica", "13"), textvariable=self.sv, validate="focusout",
                          validatecommand=self.id_entry_callback)
        self.entry1.insert(tk.END, 'ID użytkownika')
        self.entry1.pack(side=tk.LEFT, expand=True)
        self.button4 = tk.Button(master=frame, text=" + ", font=("Helvetica", "8", 'bold'), command=self.dodaj_kontakt)
        self.button4.pack(side=tk.RIGHT)

        frame = tk.Frame(
            master=self.menu,
        )
        frame.grid(row=2, column=2, pady=0, sticky="n")
        self.error_label = tk.Label(master=frame, text="", font=("Helvetica", "8"), fg='red')
        self.error_label.pack()

        frame = tk.Frame(
            master=self.menu,
            borderwidth=1
        )
        frame.grid(row=2, column=3, padx=10, pady=10)
        self.button5 = tk.Button(master=frame, fg="green", text="Zadzwoń", font=("Helvetica", "10", "bold"), command=self.zadzwon)
        self.button5.pack()

        # --------- 3 ROW ----------
        frame = tk.Frame(
            master=self.menu,
        )
        frame.grid(row=3, column=1, padx=15, sticky="w", columnspan=2)
        self.label2 = tk.Label(master=frame, text="Aktualnie rozmawiasz z:", font=("Helvetica", "8"))
        self.label2.pack()

        frame = tk.Frame(
            master=self.menu,
        )
        frame.grid(row=3, column=2, padx=15, sticky="e", columnspan=2)
        self.label3 = tk.Label(master=frame, text="Notatka o rozmówcy:", font=("Helvetica", "8"))
        self.label3.pack()

        # --------- 4 ROW ----------
        frame = tk.Frame(
            master=self.menu,
        )
        frame.grid(row=4, column=1, padx=15, pady=0, sticky="w", columnspan=2)
        self.label4 = tk.Label(master=frame, text="", font=("Consolas", "10", "bold"))
        self.label4.pack(side=tk.TOP, pady=3)
        self.button6 = tk.Button(master=frame, state='disabled', padx=20, fg="red", text="Rozłącz",
                            font=("Helvetica", "10", "bold"), command=self.rozlacz)
        self.button6.pack(side=tk.BOTTOM, pady=10)

        frame = tk.Frame(
            master=self.menu,
            borderwidth=1
        )
        frame.grid(row=4, column=2, padx=15, pady=0)
        self.button7 = tk.Button(master=frame, state='disabled', text="Wyłącz mikrofon", font=("Helvetica", "10"),
                            command=self.wylacz_mikrofon)
        self.button7.pack(side=tk.TOP)
        self.button8 = tk.Button(master=frame, state='disabled', padx=6, text="Wycisz dźwięk", font=("Helvetica", "10"),
                            command=self.wycisz_dzwiek)
        self.button8.pack(side=tk.BOTTOM, pady=10)

        frame = tk.Frame(
            master=self.menu,
            borderwidth=1
        )
        frame.grid(row=4, column=2, padx=15, pady=0, columnspan=2, sticky="ne")
        self.text1 = tk.Text(master=frame, state='disabled', height=4, width=15, font=("Helvetica", "10"))
        self.text1.pack(side=tk.TOP)

        self.thread = threading.Thread(target=self.sprawdz_pol, args=())
        self.thread.start()
        self.menu.pack()

    def spis_polaczen(self):
        spis_pol = tk.Toplevel(self.menu)
        spis_pol.title("Spis połączeń - SecurCall")
        spis_pol.resizable(False, False)

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
    def ustawienia(self):
        ustaw = tk.Toplevel(self.menu)
        ustaw.title("Ustawienia - SecurCall")

    def kontakty(self):
        def zadzwon_kontakt(key):
            kont.destroy()
            self.zadzwon_z_kontaktow(key)

        def edytuj_kontakt(key):
            def zapisz_edycje():
                c.modify_contact(key, {
                    'user_name': key,
                    'name': entry1.get(),
                    'note': text1.get("1.0", "end-1c")
                })
                kont.destroy()
                self.kontakty()

            edyt = tk.Toplevel(kont)
            edyt.title("Edycja kontaktu - SecurCall")
            edyt.resizable(False, False)

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
            self.label1 = tk.Label(master=frame, text="Edycja kontaktu", font=("Consolas", "14", "bold"))
            self.label1.pack()

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=2, column=2, padx=4, pady=10, sticky="w", columnspan=1)
            label = tk.Label(master=frame, text=testjs['contacts'][key]['user_name'], font=("Helvetica", "13"))
            label.pack(side=tk.RIGHT, expand=True)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=2, column=1, padx=10, pady=10, sticky="e")
            self.label1 = tk.Label(master=frame, text="ID", font=("Consolas", "10"))
            self.label1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=3, column=1, padx=10, pady=10, sticky="e", columnspan=2)
            entry1 = tk.Entry(master=frame, font=("Helvetica", "13"))
            if 'name' in testjs['contacts'][key]:
                entry1.insert(tk.END, testjs['contacts'][key]['name'])
            entry1.pack(side=tk.RIGHT, expand=True)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=3, column=1, padx=10, pady=10, sticky="e")
            self.label1 = tk.Label(master=frame, text="Nazwa", font=("Consolas", "10"))
            self.label1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=4, column=1, padx=10, pady=10, sticky="e", columnspan=2)
            text1 = tk.Text(master=frame, height=4, width=26, font=("Helvetica", "10"))
            if 'note' in testjs['contacts'][key]:
                text1.insert(tk.END, testjs['contacts'][key]['note'])
            text1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt,
            )
            frame.grid(row=4, column=1, padx=10, pady=10, sticky="en")
            self.label1 = tk.Label(master=frame, text="Notatka", font=("Consolas", "10"))
            self.label1.pack(side=tk.RIGHT)

            frame = tk.Frame(
                master=edyt
            )
            frame.grid(row=1, column=2, padx=10, pady=10, sticky="e")
            button1 = tk.Button(master=frame, text="Zapisz", font=("Helvetica", "10", "bold"),
                                command=zapisz_edycje)
            button1.pack(side=tk.RIGHT)

        def usun_kontakt(key):
            c.delete_contact(key)
            kont.destroy()
            self.kontakty()

        kont = tk.Toplevel(self.menu)
        kont.title("Kontakty - SecurCall")

        header = tk.Frame(kont)
        header.pack()
        k = tk.Frame(kont)
        k.pack()

        kontakt = scrollable.Scrollable(k)

        testjs = c.get_contacts()
        print(testjs)

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

        if testjs:
            rowcounter = 2
            recordcounter = 0
            labels = []
            buttons = []
            #keys = []
            for key, record in testjs['contacts'].items():
                #keys.append(key)
                print('rec ' + record['user_name'])
                frame = tk.Frame(
                    master=kontakt,
                )
                frame.grid(row=rowcounter, column=1, padx=15, pady=10, sticky="nw")
                label = tk.Label(master=frame, text=record['user_name'], font=("Consolas", "11", 'bold'))
                label.pack(side=tk.LEFT)
                labels.append(label)

                frame = tk.Frame(
                    master=kontakt,
                )
                frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="e")
                button = tk.Button(master=frame, fg="green", text="Zadzwoń", font=("Helvetica", "10", "bold"),
                                   command=partial(zadzwon_kontakt, key))
                button.pack(side=tk.LEFT)
                buttons.append(button)

                rowcounter += 1

                frame = tk.Frame(
                    master=kontakt,
                )
                frame.grid(row=rowcounter, column=1, padx=15, pady=3, sticky="nw")
                if 'name' in record:
                    label = tk.Label(master=frame, text=record['name'], font=("Helvetica", "10"))
                else:
                    label = tk.Label(master=frame, text='Brak nazwy kontaktu.', font=("Helvetica", "10"))
                label.pack(side=tk.LEFT)
                labels.append(label)

                frame = tk.Frame(
                    master=kontakt,
                )
                frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="ne")
                button = tk.Button(master=frame, padx=11, text="Edytuj", font=("Helvetica", "10"),
                                   command=partial(edytuj_kontakt, key))
                button.pack(side=tk.LEFT)
                buttons.append(button)

                rowcounter += 1

                frame = tk.Frame(
                    master=kontakt,
                )
                frame.grid(row=rowcounter, column=1, padx=15, pady=3, sticky="nw")
                if 'note' not in record or record['note'] == '':
                    label = tk.Label(master=frame, text='Brak notatki.', font=("Helvetica", "10"))
                    label.pack(side=tk.LEFT)
                    labels.append(label)
                else:
                    label = tk.Label(master=frame, text='Notatka: ' + record['note'], font=("Helvetica", "10"), wraplength=250, justify=tk.LEFT)
                    label.pack(side=tk.LEFT)
                    labels.append(label)

                frame = tk.Frame(
                    master=kontakt,
                )
                frame.grid(row=rowcounter, column=2, padx=15, pady=3, sticky="ne")
                button = tk.Button(master=frame, padx=14.5, text="Usuń", font=("Helvetica", "10"),
                                   command=partial(usun_kontakt, key))
                button.pack(side=tk.LEFT)
                buttons.append(button)

                rowcounter += 1
                recordcounter += 1

            kontakt.rowconfigure(rowcounter, weight=1, minsize=15)
            kontakt.update()

    def dodaj_kontakt(self):
        c.add_contact(self.entry1.get())

    def zadzwon_z_kontaktow(self, key):
        self.entry1.delete(0, tk.END)
        self.entry1.insert(0, key)
        res = c.make_call(self.entry1.get())
        print(res)
        c.SRTPkey = bytes.fromhex(res['srtp_security_token'])
        c.call(res['client_b_ip_addr'], res['client_b_ip_port'])

    def zadzwon(self):
        res = c.make_call(self.entry1.get())
        pprint.pprint(res)
        if res['status'] == 'OK':
            self.label4.configure(text=self.entry1.get())
            c.SRTPkey = bytes.fromhex(res['srtp_security_token'])
            c.call(res['client_b_ip_addr'], res['client_b_ip_port'])
            self.error_label['text'] = ''
            self.label4['text'] = self.entry1.get()
            self.button5.configure(state='disabled')
            self.button6.configure(state='normal')
            self.button7.configure(state='normal')
            self.button8.configure(state='normal')
        else:
            self.error_label['text'] = 'Błędne dane!'

    def rozlacz(self):
        print('Rozlacz: ' + self.label4['text'])
        tmp = c.send_bye(self.label4['text'])
        print('response: ', tmp)
        self.error_label['text'] = ''
        self.label4['text'] = ''
        self.button5.configure(state='normal')
        self.button6.configure(state='disabled')
        self.button7.configure(state='disabled')
        self.button8.configure(state='disabled')

    def wylacz_mikrofon(self):
        c.MIC_MUTED = True
        self.button7.configure(text='Włącz mikrofon', command=self.wlacz_mikrofon)

    def wlacz_mikrofon(self):
        c.MIC_MUTED = False
        self.button7.configure(text='Wyłącz mikrofon', command=self.wylacz_mikrofon)

    def wycisz_dzwiek(self):
        c.AUDIO_MUTED = True
        self.button8.configure(text='Włącz dźwięk', command=self.wlacz_dzwiek)

    def wlacz_dzwiek(self):
        c.AUDIO_MUTED = False
        self.button8.configure(text='Wycisz dźwięk', command=self.wycisz_dzwiek)

    def id_entry_callback(self):
        key = self.sv.get()
        testjs = c.get_contacts()
        if key in testjs['contacts']:
            self.text1.configure(state='normal')
            self.text1.delete("1.0", tk.END)
            self.text1.insert(tk.END, testjs['contacts'][key]['note'])
            self.text1.configure(state='disabled')

    def sprawdz_pol(self):
        def odbierz_pol():
            c.ANSWER = True
            self.label4['text'] = c.caller['user_name']
            self.error_label['text'] = ''
            self.button5.configure(state='disabled')
            self.button6.configure(state='normal')
            self.button7.configure(state='normal')
            self.button8.configure(state='normal')
            pol.destroy()
            time.sleep(1)
            global pol_exists
            pol_exists = False

        def rozlacz_pol():
            c.ANSWER = False
            pol.destroy()
            time.sleep(1)
            global pol_exists
            pol_exists = False

        global pol_exists
        pol_exists = False

        while True:
            if not c.BUSY and c.caller and 'user_name' in c.caller and not pol_exists:
                pol_exists = True
                pol = tk.Toplevel(self.menu)
                pol.columnconfigure(1, weight=1, minsize=70)
                pol.columnconfigure(2, weight=1, minsize=70)
                pol.rowconfigure(1, weight=1, minsize=50)
                pol.rowconfigure(2, weight=1, minsize=50)
                pol.rowconfigure(3, weight=1, minsize=40)

                # --------- 1 ROW ----------
                frame = tk.Frame(
                    master=pol,
                )
                frame.grid(row=1, column=1, padx=15, pady=10, sticky="we", columnspan=2)
                self.label1 = tk.Label(master=frame, text=c.caller['user_name'] + ' dzwoni do Ciebie!', font=("Helvetica", "10", 'bold'))
                self.label1.pack()

                frame = tk.Frame(
                    master=pol,
                    borderwidth=1
                )
                frame.grid(row=2, column=1, pady=10, padx=15)
                self.button1 = tk.Button(master=frame, fg="green", text="Odbierz", font=("Helvetica", "10", 'bold'),
                                         command=odbierz_pol)
                self.button1.pack()
                frame = tk.Frame(
                    master=pol,
                    borderwidth=1
                )
                frame.grid(row=2, column=2, pady=10, padx=15)
                self.button2 = tk.Button(master=frame, fg="red", text="Rozłącz", font=("Helvetica", "10", 'bold'),
                                         command=rozlacz_pol)
                self.button2.pack()

            if c.GOT_BYE:
                self.error_label['text'] = ''
                self.label4['text'] = ''
                self.button5.configure(state='normal')
                self.button6.configure(state='disabled')
                self.button7.configure(state='disabled')
                self.button8.configure(state='disabled')
                c.GOT_BYE = False

            time.sleep(1)


def set_frame(new_frame, is_main_menu=False):
    global current

    # hide current tk.Frame
    current.pack_forget()

    if is_main_menu:
        mm = main_menu(root, img)
    # show new tk.Frame
    else:
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
    root.mainloop()

