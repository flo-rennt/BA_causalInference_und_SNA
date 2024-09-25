# BA_FSeuffert_2024 - Python Code zu Datenauswertung und Community Detecton für meine Bachelorarbeit

## Daten_Paper_FanningTheFlames

Um zu evaluieren wie viele Angriffe während der 313 Internetausfälle stattfanden, habe ich die Daten der Studie ausgewertet. Die Daten sind veröffentlicht unter [1] (am Ende der Seite). Aufgrund ihrer Größe können diese nicht im Github Ordner mit abgelegt werden und müssen unter [1] abgerufen werden.

Vorgehen

0. Datendownload von [1]
1. Python Script load\_dta.py ausführen. Es überträgt die .dta Dateien im DATA-Ordner in csv-Dateien.
2. Die für uns relevanten Daten befinden sich in reproduction\_panel_clean.csv
3. Python Script findNumberOfOutages.py ausführen, um zu ermitteln wie viele Angriffe es während der 313 Internetausfälle gab.
4. Ergebnis: Keine.

[1] https://academic.oup.com/jeea/article/19/4/2131/5917396?guestAccessKey=00cfbf48-1ff4-4962-b5d9-2a9ed9276ef3&login=false


## CommunityDetection

Der Datensatz datensatz.csv mit TikTokDaten wird durch das Python-Skript datensatzGenerator.py um die Spalten account-id und follows ergänzt. 
Auf diesem nun bzgl. Follow-Relation synthetischen Datensatz daten-syn.csv werden die Algorithmen "Walktrap", "Louvain" und "Girvan-Newman" ausgeführt: CommunityDetection\_Walktrap\_Girvan\_Louvain.py
Die Ergebnisse sind in den jpgs visualisiert.
