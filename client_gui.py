import tkinter as tk


def create_main_menu(menu, logo):
    def spis_polaczen():
        spis = tk.Toplevel(menu)
        spis.title("Spis połączeń - SecurCall")


    def ustawienia():
        ustaw = tk.Toplevel(menu)
        ustaw.title("Ustawienia - SecurCall")

    def kontakty():
        kontakt = tk.Toplevel(menu)
        kontakt.title("Kontakty - SecurCall")

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
    label4 = tk.Label(master=frame, text="Jan Kowalski", font=("Helvetica", "10", "bold"))
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

