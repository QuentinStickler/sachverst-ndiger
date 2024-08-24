import pandas as pd

# Lade die CSV-Datei in ein DataFrame
data = pd.read_csv("Data_Original.csv", sep="|", encoding="utf-16-LE")

# Entferne führende und nachfolgende Leerzeichen aus dem "Timestamp"
data["Timestamp"] = data["Timestamp"].str.strip()

# Konvertiere die "Timestamp"-Spalte in das Datetime-Format
data["Timestamp"] = pd.to_datetime(data["Timestamp"], utc=True)

# Extrahiere die Stunden- und Minuteninformation aus dem Zeitstempel
data["Hour"] = data["Timestamp"].dt.hour
data["Minute"] = data["Timestamp"].dt.minute

# Gruppiere die Daten nach "Sender Name", "Hour" und "Minute" und zähle die Nachrichten
activity_by_minute = data.groupby(["Sender Name", "Hour", "Minute"]).size().unstack(fill_value=0)

# Berechne die Korrelationen zwischen den Aktivitätsprofilen der Absender
senders = activity_by_minute.index
sender_correlation_df = pd.DataFrame(index=senders, columns=senders)

for i, sender1 in enumerate(senders):
    for j in range(i + 1, len(senders)):
        sender2 = senders[j]
        correlation = activity_by_minute.loc[sender1].corr(activity_by_minute.loc[sender2])
        sender_correlation_df.at[sender1, sender2] = correlation
        sender_correlation_df.at[sender2, sender1] = correlation

# Speichere die Korrelationsergebnisse in einer CSV-Datei
sender_correlation_df.to_csv("sender_correlation_results.csv")

# Filtere Korrelationen größer als 0.8
high_correlation_df = sender_correlation_df[sender_correlation_df > 0.8].stack().reset_index()
high_correlation_df.columns = ["Sender1", "Sender2", "Correlation"]

# Speichere die hochkorrelierten Ergebnisse in einer CSV-Datei
high_correlation_df.to_csv("high_correlation_results.csv", index=False)

# Analyse der Pausen- und Antwortzeiten
data["Next Timestamp"] = data.groupby("Sender Name")["Timestamp"].shift(-1)
data["Response Time"] = (data["Next Timestamp"] - data["Timestamp"]).dt.total_seconds() / 60.0  # in Minuten

# Pausenmuster (z.B. mittlere Pausenzeit)
pause_patterns = data.groupby("Sender Name")["Response Time"].median()

# Speichere die Pausenmuster in einer CSV-Datei
pause_patterns.to_csv("pause_patterns.csv")
