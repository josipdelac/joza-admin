# process_b.py

import os
import camelot
import pandas as pd
import sys

def main(excel_izlazna_putanja, pdf_direktorijum):
    # Putanja do direktorijuma sa PDF fajlovima
    pdf_direktorijum = pdf_direktorijum

    # Lista za skladištenje svih redova, gde svaki red sadrži tablice iz jednog PDF dokumenta
    svi_redovi = []

    # Lista za skladištenje svih putanja
    sve_putanje = []

    # Pretraživanje svih PDF fajlova u direktorijumu
    for filename in os.listdir(pdf_direktorijum):
        if filename.endswith(".pdf"):
            pdf_putanja = os.path.join(pdf_direktorijum, filename)

            print(f"Trenutno sam na '{filename}' kojeg obrađujem.")

            # Izvlačenje svih tablica iz PDF-a pomoću Camelot
            parametri_camelot = {
                'flavor': 'lattice',   # Koristi lattice flavor za prepoznavanje tablica
                'line_scale': 40,      # Prilagodi osetljivost na linije
            }
            tables = camelot.read_pdf(pdf_putanja, **parametri_camelot)

            # Kreiranje reda sa svim tablicama iz trenutnog PDF dokumenta
            red_tablica = []
            for table in tables:
                if table.df.shape[0] > 1:  # Proveravamo da li ima drugih redova
                    redak_df = table.df.iloc[1]  # Drugi redak
                    red_tablica.extend(redak_df.values.tolist())

            # Dodavanje reda sa svim tablicama u listu svi_redovi
            svi_redovi.append(red_tablica)
            sve_putanje.append(pdf_putanja)

    # Sačuvajte sve redove i putanje u Excel fajl sa naslovima kolona
    naslovi_kolona = ['Ime i Prezime', 'Datum rođenja', 'Osobni broj', 'OIB', 'Naziv obveznika', 'OIB', 'Adresa', 'Datum stjecanja svojstva osiguranika', 'Osnova osiguranja']
    excel_izlazna_putanja = excel_izlazna_putanja
    try:
        svi_redovi_df = pd.DataFrame(svi_redovi, columns=naslovi_kolona)
        svi_redovi_df['PDF Putanja'] = sve_putanje
        svi_redovi_df.to_excel(excel_izlazna_putanja, index=False)
        print(f"Sve tablice iz svih PDF dokumenata sa putanjama su sačuvane u '{excel_izlazna_putanja}'.")
    except Exception as e:
        print(f"Greška prilikom čuvanja u Excel fajl: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python process_b.py excel_izlazna_putanja pdf_direktorijum")
        sys.exit(1)
    
    excel_izlazna_putanja = sys.argv[1]
    pdf_direktorijum = sys.argv[2]
    main(excel_izlazna_putanja, pdf_direktorijum)
