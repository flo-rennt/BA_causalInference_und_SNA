# BA_FSeuffert_2024 - Python Code zu Datenauswertung und Community Detecton für meine Bachelorarbeit

## Daten_Paper_FanningTheFlames

Um zu evaluieren wie viele Angriffe während der 313 Internetausfälle stattfanden, habe ich die Daten der Studie ausgewertet. Die Daten sind veröffentlicht unter [1] (am Ende der Seite). Aufgrund ihrer Größe können diese nicht im Github Ordner mit abgelegt werden und müssen unter [1] abgerufen werden.

Vorgehen
0. Datendownload von [1]
1. Python Script load\_dta.py ausführen. Es überträgt die .dta Dateien im DATA-Ordner in csv-Dateien.
2. Die für uns relevanten Daten befinden sich in reproduction\_panel_clean.csv
3. Python Script findNumberOfOutages.py ausführen, um zu ermitteln wie viele Angriffe es während der 313 Internetausfälle gab.
4. Ergebnis: Keine.

Erläuterungen: 

Wenn ihr die Dateien aus [1] abspeichert und dann das Pyhton Skript load\_dta.py im gleichen Ordner wie die .dta Dateien speichert und ausführt, werden diese in .csv Dateien umgewandelt, die sich leicht öffnen und ihr Inhalt besser einschätzen lässt. Die relevanten Daten liegen in reproduction\_panel\_clean.csv, wobei es hier einige Spalten für Angriffe und Internetausfälle gibt. Ein Blick in die Datei reproduction\_file\_Fanning\_Flames\_Hate\_clean.do lässt vermuten, dass wir die Spalte CO brauchen mit dem Label internet\_outage\_p75 (Es wurde label var internet\_outage_p75 „Internet outage“ definiert). Da nun bekannt ist in welchen Spalten die wichtigen Informationen liegen, kann ein Python Skript erstellt werden dass auf diesen Spalten die Filterung ausführt und wir somit die Anzahl aller Wochen-Gemeinden Paare ermitteln können in denen Internetausfälle und Angriffe auf Geflüchtete zusammenfielen. 


[1] https://academic.oup.com/jeea/article/19/4/2131/5917396?guestAccessKey=00cfbf48-1ff4-4962-b5d9-2a9ed9276ef3&login=false


## CommunityDetection

Auf dem synthetischen Datensatz tt\_outlet\_sample.csv werden die Algorithmen "Walktrap", "Louvain" und "Girvan-Newman" ausgeführt: CommunityDetection\_Walktrap\_Girvan\_Louvain.py
Die Ergebnisse sind in den jpgs visualisiert.
