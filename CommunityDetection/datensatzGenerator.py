import pandas as pd
import random

# TikTok Datensatz öffnen
df = pd.read_csv('datensatz.csv')

# Account-id spalte mit Nummerierung 1 bis 100
df['account-id'] = range(1, 101)

# Follows enthält alle Accounts denen der Account folgt
# random.randint liefert eine zufällige Anzahl an Accounts, denen gefolgt wird
# random.sample dazugehörige zufällge Auswahl an ids
def generate_follows(id_value):
    number = random.randint(1, 8)
    follows = random.sample([i for i in range(1, 101) if i != id_value], number)
    return ','.join(map(str, follows))

df['follows'] = df['account-id'].apply(generate_follows)

# neuer teils synthetischer Datensatz in daten-syn.csv gespeichert
df.to_csv('daten-syn.csv', index=False)
