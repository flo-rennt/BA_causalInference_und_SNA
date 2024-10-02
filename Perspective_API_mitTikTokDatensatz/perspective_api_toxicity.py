import csv
from googleapiclient import discovery
import json

# Deine API-Schlüssel
API_KEY = 'AIzaSyDC6ZJhkih9yo9nbGykq_AxY_n34zQvhnY'

# CSV-Datei und Spaltennamen
csv_file_path = 'tt_outlet_sample.csv'
text_column_name = 'voice_to_text'
id_column_name = 'id'
output_file_path = 'toxicity_scores.txt'

# Google API Client initialisieren
client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

# Datei zum Schreiben öffnen
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Überschrift der Tabelle schreiben
    output_file.write("ID\tToxicity Score (%)\n")
    output_file.write("-" * 30 + "\n")

    # CSV-Datei öffnen und Zeilen durchlaufen
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Für jede Zeile in der CSV
        for row in reader:
            comment_id = row[id_column_name]
            comment_text = row[text_column_name].strip()  # Entfernt führende und nachfolgende Leerzeichen
            
            # Sicherstellen, dass der Kommentar nicht leer ist
            if comment_text:
                # Request für die Perspective API vorbereiten
                analyze_request = {
                    'comment': { 'text': comment_text },
                    'requestedAttributes': {'TOXICITY': {}}
                }

                try:
                    # API-Aufruf zur Analyse des Kommentars
                    response = client.comments().analyze(body=analyze_request).execute()
                    
                    toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value'] * 100

                    # Ergebnis in die Datei schreiben
                    output_file.write(f"{comment_id}\t{toxicity_score:.2f}%\n")
                except Exception as e:
                    # Fehler in die Datei schreiben
                    output_file.write(f"{comment_id}\tFehler: {str(e)}\n")
            else:
                # Leere Kommentare überspringen und in die Datei schreiben
                output_file.write(f"{comment_id}\t-\n")

print(f"Analyse abgeschlossen. Ergebnisse in '{output_file_path}' gespeichert.")
