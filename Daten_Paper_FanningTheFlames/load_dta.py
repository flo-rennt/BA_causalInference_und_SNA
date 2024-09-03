import pandas as pd
import os

# Pfad zum Verzeichnis
directory = './' 

# Durch alle Dateien im Verzeichnis iterieren
for filename in os.listdir(directory):
    if filename.endswith('.dta'):
        # Pfad zur Datei erstellen
        file_path = os.path.join(directory, filename)
        
        # .dta Datei einlesen
        data = pd.read_stata(file_path)
        
        # Dateiname ohne die .dta Endung
        base_filename = os.path.splitext(filename)[0]
        
        # Neuen Dateinamen für die CSV-Datei erstellen und Speicherort festlegen
        csv_filename = f'{base_filename}.csv'
        csv_path = os.path.join(directory, csv_filename)
        
        # Daten als CSV-Datei speichern
        data.to_csv(csv_path, index=False)
        
        #Konsolenausgabe
        print(f'Konvertiert: {filename} -> {csv_filename}')

