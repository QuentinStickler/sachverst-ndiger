import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Lade die CSV-Datei in ein DataFrame
data = pd.read_csv("Data_Original.csv", sep="|", encoding="utf-16-LE")

# Entferne führende und nachfolgende Leerzeichen aus dem "Timestamp"-String
data["Timestamp"] = data["Timestamp"].str.strip()

# Konvertiere die "Timestamp"-Spalte in das datetime-Format
data["Timestamp"] = pd.to_datetime(data["Timestamp"], utc=True)

# Extrahiere die Stundeninformation aus dem Zeitstempel
data["Hour"] = data["Timestamp"].dt.hour

# Gruppiere die Daten nach "Sender Name" und "Hour" und zähle die Nachrichten pro Stunde
sender_activity_profiles = data.groupby(["Sender Name", "Hour"]).size().unstack(fill_value=0)

# Berechne die Kosinusähnlichkeit zwischen den Aktivitätsprofilen aller Sender
similarity_matrix = cosine_similarity(sender_activity_profiles)

# Erstelle ein DataFrame aus der Ähnlichkeitsmatrix
similarity_df = pd.DataFrame(similarity_matrix, 
                             index=sender_activity_profiles.index, 
                             columns=sender_activity_profiles.index)

# Umwandlung der Ähnlichkeitsmatrix in Paare, ohne Stack-Funktion
similarity_pairs = []

# Iteriere über alle Sender, um Paare zu erstellen
senders = similarity_df.index
for i in range(len(senders)):
    for j in range(i + 1, len(senders)):  # Beachte: j beginnt bei i + 1, um doppelte Paare zu vermeiden
        similarity_pairs.append({
            'Sender 1': senders[i],
            'Sender 2': senders[j],
            'Similarity': similarity_df.iloc[i, j]
        })

# Konvertiere die Paare in ein DataFrame
similarity_pairs_df = pd.DataFrame(similarity_pairs)

# Filtere die Ähnlichkeitsdaten nach einem Schwellenwert, z.B. 0.8
high_similarity_df = similarity_pairs_df[similarity_pairs_df['Similarity'] > 0.8]

# Speichere die Ergebnisse in einer CSV-Datei
output_file = "high_cosine_similarity_results.csv"
high_similarity_df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Sender pairs with cosine similarity higher than 0.8 have been saved to {output_file}")
