## Gruppenlösungen der Aufgaben

### Aufgabe 1:
Basic Statistics: Bitte setzen Sie sich mit dem Datensatz grundlegend auseinander und verschaffen sich einen Überblick über die Texte, Videos, Fotoaufnahmen, die darin enthalten sind. Gehen Sie dabei auf Fragen ein, wie: Wie viele Fotoaufnahmen beinhaltet der Datensatz, wie viele Texte werden insgesamt versandt, wie viele pro Person? Wie viele Kommunikationsteilnehmer gibt es? Welche Person sendet die meisten Texte/Fotos? Welche Person erhält die meisten Nachrichten? 

#### Anzahl und Art der Attachments:
Lösung durch filecrawler.py Program. Erstellt eine Liste für jedes Dateiformat und zählt anschließend diese.
#### Wie viele Fotoaufnahmen beinhaltet der Datensatz?
Number of .jpg Files: 985
Number of .png Files: 106
(Number of .txt Files: 11, Text Dateien zu nicht jugendfreien Bildern)
#### Wie viele Videos beinhaltet der Datensatz?
Number of .mp4 Files: 73
Number of .gif Files: 8

Number of other Files: 2

#### Erstellen einer CSV Datei zur statistischen Auswertung der json Datei, die alle Nachrichten und Meta Daten enthält.
    1. Erstellen von Listen der gewünschten Keys der json Datei, mittels Commandline Tool jq (https://jqlang.github.io/jq/). (sender names, sender appid, recipient names, recipient appid, message text, message time, message direction)
        Befehle für jq:
          jq '.Images[].Artifacts[].[].[].[].Sender.Name' .\Case_DarkNight.json | Out-File sender_names_all.txt
          jq '.Images[].Artifacts[].[].[].[].Sender.AppId' .\Case_DarkNight.json | Out-File sender_appid_all.txt
          jq '.Images[].Artifacts[].[].[].[].Time' .\Case_DarkNight.json | Out-File message_time_all.txt
          jq '.Images[].Artifacts[].[].[].[].Text' .\Case_DarkNight.json | Out-File message_text_all.txt
          jq '.Images[].Artifacts[].[].[].[].Direction' .\Case_DarkNight.json | Out-File message_direction_all.txt
          jq '.Images[].Artifacts[].[].[].[].Attachment' .\Case_DarkNight.json | Out-File message_attachment_all.txt
          jq '.Images[].Artifacts[].[].[].[].Recipients[].AppId' .\Case_DarkNight.json | Out-File recipient_AppId_all.txt
          jq '.Images[].Artifacts[].[].[].[].Recipients[].Name' .\Case_DarkNight.json | Out-File recipient_name_all.txt
    2. Kopieren in Excel Datei
    3. Mittels CONCATENATE einzelne Spalten zusammenfügen. Dabei wird ein | als seperator eingefügt, da die Texte innerhalb der Nachrichten ein , enthalten. Anschließend in Notepad als CSV speichern.
    4. Mittels des Read CSV Operators die CSV Datei in Rapidminer einlesen, dabei den seperator auf | stellen und die Textformatierung auf UTF-16-LE stellen.

    
#### Wie viele Texte (Nachrichten) werden versandt?
Insgesamt 3369 Zeilen in der CSV (Nachrichten)
Davon 941 Missing Values -> Insgesamt 2428 Textnachrichten

#### Pro Person?
Siehe Excel Tabelle
Durchschnittlich 104 bei Sendern

#### Anzahl an Kommunikationsteilnehmer?
34 (Anhand der Sender und Recipient Names)
siehe Excel Tabelle

#### Welche Person sendet die meisten Nachrichten?
Maverick SOB -> 601 Nachrichten

#### Welche Person empfängt die meisten Nachrichten?
Stockholm Stealers -> 558
