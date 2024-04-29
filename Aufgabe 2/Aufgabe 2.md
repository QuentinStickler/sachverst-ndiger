# Aufgabe 2
Aktivitätsprofile: Aufbauend auf Aufgabe 1 - 
Basic Statistics sollen nun Aktivitätsprofile der einzelnen Nutzer erarbeitet werden. Die Aktivitätsprofile sollen dabei unter anderem beinhalten: 
1. In welchen Zeiträumen am Tag senden die einzelnen Nutzer Nachrichten? 
2. In welchen Zeiträumen erhalten die einzelnen Nutzer Nachrichten? 
3. Lassen sich aus den Zeiträumen bevorzugte Aktivitätszeiten ableiten? 
4. Lassen sich Gemeinsamkeiten in den Aktivitätszeiten zwischen einzelnen Nutzern feststellen? 
5. Lässt sich eine Dauer bis eine Nachricht durch den Nutzer beantwortet wird ableiten? 
6. Verwenden die einzelnen Nutzer nur Schriftzeichen zum Senden von Nachrichten oder aktiv ebenfalls auch Fotos? 
7. Lassen sich Gruppen von Nutzern bilden, die ähnliche Aktivitätszeiten aufweisen? 
8. Lassen sich Nutzer mit ähnlichen Chatnamen in diversen Messengern, über mehrere Mobilgeräte hinweg, als ein und dieselbe Person durch die Aktivitätsprofile identifizieren?

### Bearbeitung der Aufgabe

#### In welchen Zeiträumen am Tag senden die einzelnen Nutzer Nachrichten?
[Python Programm Aktivitätsanalyse.py](Aktivitätsanalyse.py)

`activity_profile = data.groupby([data["Sender Name"].str.strip(), "Hour"]).size().unstack(fill_value=0)`

Erstellt für jeden Sender eine Tabelle, in welcher Stunde er wie viele Nachrichten geschrieben hat.

[Histogramme Sender](activity_profiles_images)


#### In welchen Zeiträumen erhalten die einzelnen Nutzer Nachrichten?
[Python Programm Aktivitätsanalyse Empfang.py](https://github.com/QuentinStickler/sachverst-ndiger/blob/main/Aufgabe%202/Aktivit%C3%A4tsanalyse%20Empfang.py)

`received_messages = data.groupby(["Recipient Name", "Hour"]).size().unstack(fill_value=0)`

Erstellt für jeden Empfänger eine Tabelle, in welcher Stunde er wie viele Nachrichten bekommen hat.


#### Lassen sich aus den Zeiträumen bevorzugte Aktivitätszeiten ableiten?
[Python Programm preferred_activity_time.py](preferred_activity_time.py)

`activity_profile = data.groupby([data["Sender Name"].str.strip(), "Hour"]).size().unstack(fill_value=0)`
`preferred_activity_time = sender_activity_profiles.idxmax(axis=1)`

Gibt die Stunde mit den höchsten gesendeten Nachrichten am Tag für jeden Nutzer aus.

[CSV Ergebnis preferred_activity_time.csv](preferred_activity_time.py)


#### Lassen sich Gemeinsamkeiten in den Aktivitätszeiten zwischen einzelnen Nutzern feststellen?

Noch nicht komplett bearbeitet.


#### Lässt sich eine Dauer bis eine Nachricht durch den Nutzer beantwortet wird ableiten?
[Python Programm response_time.py](response_time.py)

`average_response_times = response_times.groupby(["Sender Name", "Recipient Name"]).mean()`

Berechnet die Durchschnittliche Zeit ein Nutzer braucht nachdem er eine Nachricht von jemanden anderen bekommen hat.

[CSV Ergebnis average_response_times.csv](average_response_times.csv)


#### Verwenden die einzelnen Nutzer nur Schriftzeichen zum Senden von Nachrichten oder aktiv ebenfalls auch Fotos?

Noch nicht bearbeitet.


#### Lassen sich Gruppen von Nutzern bilden, die ähnliche Aktivitätszeiten aufweisen?
[Python Programm activity_time_sender_correlation.py](activity_time_sender_correlation.py)

Berechnet die Korrelation zwischen den verschiedenen Sendern anhand der gesendeten Nachrichten pro Stunde.

[CSV Ergebnis sender_correlation_result.csv](sender_correlation_result.csv)
[CSV Ergebnis high_correlation_result.csv](high_correlation_result.csv)


#### Lassen sich Nutzer mit ähnlichen Chatnamen in diversen Messengern, über mehrere Mobilgeräte hinweg, als ein und dieselbe Person durch die Aktivitätsprofile identifizieren?

Noch nicht bearbeitet.
