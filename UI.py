import tkinter as tk
from tkinter import ttk

def create_interface(get_text_callback):
    # Creează fereastra principală
    root = tk.Tk()
    root.title("Prețuri Combustibili - Comparație")
    root.geometry("800x500")
    root.configure(bg="#e9f5f9")  # Fundal pastel deschis

    # Titlu aplicație
    title_label = tk.Label(
        root,
        text="Comparație Prețuri Combustibili",
        font=("Arial", 18, "bold"),
        bg="#e9f5f9",
        fg="#004d66"  # Albastru închis
    )
    title_label.pack(pady=20)

    # Cadru pentru elementele de intrare
    frame = tk.Frame(root, bg="#e9f5f9")
    frame.pack(pady=30)

    # Eticheta și TextBox pentru Oraș 1
    label1 = tk.Label(
        frame,
        text="Oraș 1:",
        font=("Arial", 14),
        bg="#e9f5f9",
        fg="#333333"
    )
    label1.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    text_box1 = ttk.Entry(frame, width=40, font=("Arial", 12))
    text_box1.grid(row=0, column=1, padx=10, pady=10)

    # Eticheta și TextBox pentru Oraș 2
    label2 = tk.Label(
        frame,
        text="Oraș 2:",
        font=("Arial", 14),
        bg="#e9f5f9",
        fg="#333333"
    )
    label2.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    text_box2 = ttk.Entry(frame, width=40, font=("Arial", 12))
    text_box2.grid(row=1, column=1, padx=10, pady=10)

    # Creează stilul personalizat pentru buton
    style = ttk.Style()
    style.configure(
        "Custom.TButton",
        font=("Arial", 12),
        padding=5,
        foreground="black",  # Text negru
        background="#e0e0e0",  # Fundal gri deschis
        borderwidth=1
    )
    style.map(
        "Custom.TButton",
        background=[("active", "#cfcfcf")],  # Fundal mai închis la hover
        foreground=[("active", "black")],  # Text negru la hover
        relief=[("pressed", "sunken")]  # Efect vizual la click
    )

    # Butonul de căutare
    get_text_button = ttk.Button(
        root,
        text="Caută prețuri",
        command=lambda: get_text_callback(text_box1.get().strip(), text_box2.get().strip()),
        style="Custom.TButton"  # Folosește stilul personalizat
    )
    get_text_button.pack(pady=20)

    # Footer
    footer_label = tk.Label(
        root,
        text="Aplicație creată pentru a compara prețurile combustibililor în orașele alese.",
        font=("Arial", 10, "italic"),
        bg="#e9f5f9",
        fg="#666666"
    )
    footer_label.pack(side="bottom", pady=10)

    # Stilizare pentru ttk.Widget
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=5, background="#007b99", foreground="white")
    style.configure("TEntry", padding=5)

    # Rulează aplicația
    root.mainloop()