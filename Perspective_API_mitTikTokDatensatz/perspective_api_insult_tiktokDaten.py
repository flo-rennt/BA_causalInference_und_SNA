import csv
from googleapiclient import discovery
import json

# Deine API-Schlüssel
API_KEY = 'AIzaSyDC6ZJhkih9yo9nbGykq_AxY_n34zQvhnY'

# CSV-Datei und Spaltennamen
csv_file_path = 'tt_outlet_sample.csv'
text_column_name = 'voice_to_text'
id_column_name = 'id'
output_file_path = 'identity_attack_scores.txt'

# Google API Client initialisieren
client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Überschrift
    output_file.write("ID\tIdentity Attack Score (%)\n")
    output_file.write("-" * 30 + "\n")

    # CSV-Datei öffnen und Zeilen durchlaufen
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            comment_id = row[id_column_name]
            comment_text = row[text_column_name].strip()  
            
            # nicht leere Kommentare überspringen
            if comment_text:
            
                analyze_request = {
                    'comment': { 'text': comment_text },
                    'requestedAttributes': {'IDENTITY_ATTACK': {}}
                }

                try:
                    # API-Aufruf zur Analyse 
                    response = client.comments().analyze(body=analyze_request).execute()
                    
                    identity_attack_score = response['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value'] * 100

                    output_file.write(f"{comment_id}\t{identity_attack_score:.2f}%\n")
                except Exception as e:
                    output_file.write(f"{comment_id}\tFehler: {str(e)}\n")
            else:
                output_file.write(f"{comment_id}\tLeerer Kommentar\n")

print(f"Die Ergebnisse der Identity-Attack Analyse sind in '{output_file_path}' gespeichert.")
