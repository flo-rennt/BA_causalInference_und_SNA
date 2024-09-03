import pandas as pd
import numpy as np

# CSV-Datei laden
dataFile = pd.read_csv('reproduction_panel_clean.csv')

# Toleranzwert für 0.0 Vergleich
epsilon = 1e-10

# Filtern um die Outages (p75) zu erhalten
gefiltert_internet_outage = dataFile[np.abs(dataFile['internet_outage_p75'] - 0.0) > epsilon]
anzahl_internet_outage = len(gefiltert_internet_outage)
unique_municipalities = len(gefiltert_internet_outage.drop_duplicates(subset='kreis_code'))

# Wochen mit Internet-Outage und (mind. 1) Angriff versus Wochen ohne Angriff
mit_angriff = dataFile[(np.abs(dataFile['internet_outage_p75'] - 0.0) > epsilon) & (dataFile['refugee_attacks'] != 0)]
ohne_angriff = dataFile[(np.abs(dataFile['internet_outage_p75'] - 0.0) > epsilon) & (dataFile['refugee_attacks'] == 0)]
anzahl_mit = len(mit_angriff)
anzahl_ohne = len(ohne_angriff)

print(f"Es gab {anzahl_internet_outage} viele Internetausfälle.")
print(f"Diese verteilen sich (basierend auf Unterschiede im Eintrag 'kreis_code') auf {unique_municipalities} Gemeinden.")
if anzahl_mit > 0:
    print(f"Während den {anzahl_internet_outage} Outages sind in {anzahl_mit} Wochen-Gemeinde-Paaren Angriffe passiert und in {anzahl_ohne} Wochen keine Angriffe.")
else: 
    print(f"Während der {anzahl_internet_outage} Outages sind keine Angriffe in den betroffenen Wochen-Gemeinde-Paaren vorgefallen.")    