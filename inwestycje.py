import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from math import ceil

def oblicz_inwestycje():
    try:
        poczatkowa_wplata = float(entry_poczatkowa.get())
        miesieczna_wplata = float(entry_miesieczna.get())
        roczna_stopa = float(entry_stopa.get()) / 100
        okres = int(entry_okres.get())
        
        kapital = poczatkowa_wplata
        miesieczna_stopa = roczna_stopa / 12
        miesiace = okres * 12
        historia = []

        for _ in range(miesiace):
            kapital += miesieczna_wplata
            kapital *= (1 + miesieczna_stopa)
            historia.append(kapital)

        suma_wplat = poczatkowa_wplata + miesiace * miesieczna_wplata
        zysk = kapital - suma_wplat

        wynik_label.config(text=f"Wartość inwestycji: {kapital:.2f} zł\n"
                                f"Suma wpłat: {suma_wplat:.2f} zł\n"
                                f"Zysk: {zysk:.2f} zł")
        return historia, kapital, suma_wplat, zysk
    except ValueError:
        messagebox.showerror("Błąd", "Podaj prawidłowe wartości liczbowe!")
        return None

def generuj_wykres():
    wynik = oblicz_inwestycje()
    if wynik:
        historia, _, _, _ = wynik
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(historia) + 1), historia, label="Wartość inwestycji", color="blue")
        plt.title("Wzrost wartości inwestycji w czasie")
        plt.xlabel("Miesiące")
        plt.ylabel("Wartość inwestycji (zł)")
        plt.grid(True)
        plt.legend()
        plt.show()

def zapisz_wyniki():
    wynik = oblicz_inwestycje()
    if wynik:
        historia, kapital, suma_wplat, zysk = wynik
        
        plik_wyniki = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Plik tekstowy", "*.txt")])
        if not plik_wyniki:
            return
        
        with open(plik_wyniki, "w") as f:
            f.write("=== Wyniki inwestycji ===\n")
            f.write(f"Wartość inwestycji: {kapital:.2f} zł\n")
            f.write(f"Suma wpłat: {suma_wplat:.2f} zł\n")
            f.write(f"Zysk: {zysk:.2f} zł\n")

        # Zapis wykresu
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(historia) + 1), historia, label="Wartość inwestycji", color="blue")
        plt.title("Wzrost wartości inwestycji w czasie")
        plt.xlabel("Miesiące")
        plt.ylabel("Wartość inwestycji (zł)")
        plt.grid(True)
        plt.legend()
        
        plik_wykres = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Plik graficzny", "*.png")])
        if not plik_wykres:
            return
        plt.savefig(plik_wykres)
        messagebox.showinfo("Sukces", "Wyniki i wykres zostały zapisane!")

root = tk.Tk()
root.title("Kalkulator Inwestycji")
root.geometry("800x400")

tk.Label(root, text="Wpłata początkowa (zł):").grid(row=0, column=0, padx=10, pady=5)
entry_poczatkowa = tk.Entry(root)
entry_poczatkowa.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Miesięczna wpłata (zł):").grid(row=1, column=0, padx=10, pady=5)
entry_miesieczna = tk.Entry(root)
entry_miesieczna.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Roczna stopa zwrotu (%):").grid(row=2, column=0, padx=10, pady=5)
entry_stopa = tk.Entry(root)
entry_stopa.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Okres inwestycji (lata):").grid(row=3, column=0, padx=10, pady=5)
entry_okres = tk.Entry(root)
entry_okres.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Oblicz i pokaż wyniki", command=oblicz_inwestycje).grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(root, text="Generuj wykres", command=generuj_wykres).grid(row=5, column=0, columnspan=2, pady=10)

tk.Button(root, text="Pobierz wyniki i wykres", command=zapisz_wyniki).grid(row=6, column=0, columnspan=2, pady=10)

wynik_label = tk.Label(root, text="", fg="green", justify="left")
wynik_label.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
