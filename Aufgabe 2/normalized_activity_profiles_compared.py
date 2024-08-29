import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Create a folder to store the images if it doesn't exist
output_folder = "activity_profiles_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lade die CSV-Datei in ein DataFrame
data = pd.read_csv("Data_Original.csv", sep="|", encoding="utf-16-LE")

# Remove leading and trailing spaces from the "Timestamp" string
data["Timestamp"] = data["Timestamp"].str.strip()

# Convert the "Timestamp" column to datetime format
data["Timestamp"] = pd.to_datetime(data["Timestamp"], utc=True)

# Extrahieren der Stundeninformation aus dem Zeitstempel
data["Hour"] = data["Timestamp"].dt.hour

# Group the data by "Sender Name" (case-sensitive) and "Hour" and count the messages per hour
activity_profile = data.groupby([data["Sender Name"].str.strip(), "Hour"]).size().unstack(fill_value=0)

# Liste der Sender, für die ein Histogramm erstellt werden soll
senders = ["Twi Grey", "Twilight G", "Twilight Grey", "TwilightGrey"]  # Ersetze diese Liste durch die gewünschten Sender

# Normalisieren der Nachrichtenzahlen pro Sender
normalized_activity_profile = activity_profile.div(activity_profile.sum(axis=1), axis=0)

# Farbpalette für die Sender
cmap = plt.get_cmap('tab10')  # Lade die Colormap 'tab10'
colors = [cmap(i) for i in range(len(senders))]  # Erzeuge eine Liste von Farben basierend auf der Anzahl der Sender

# Filtern der Daten für die ausgewählten Sender
filtered_activity_profile = normalized_activity_profile.loc[senders]

# Plotten des kombinierten normalisierten Histogramms
plt.figure(figsize=(16, 8))  # Vergrößere das Diagramm, um mehr Platz zu haben

# Breite der Balken
bar_width = 0.2

# Abstand zwischen den Gruppen von Balken
spacing = 0.8

# Positionsliste für die Balken der ersten Gruppe
r = np.arange(len(filtered_activity_profile.columns)) * (bar_width * len(senders) + spacing)

# Plotten der Balken für jeden Sender
for idx, sender_name in enumerate(senders):
    if sender_name in filtered_activity_profile.index:
        plt.bar(r + idx * bar_width, filtered_activity_profile.loc[sender_name], color=colors[idx], width=bar_width, edgecolor='grey', label=sender_name)

# Hinzufügen von vertikalen Trennlinien zwischen den Stunden
for pos in r:
    plt.axvline(x=pos - (spacing / 2), color='black', linestyle='--', linewidth=0.5)

# Hinzufügen von Titeln und Labels
plt.title("Normalized Activity Profile per Hour")
plt.xlabel("Hour of the Day")
plt.ylabel("Relative Frequency of Messages")
plt.xticks([pos + bar_width * (len(senders)-1)/2 for pos in r], filtered_activity_profile.columns)
plt.legend()

# Speichern des kombinierten Histogramms
output_path = os.path.join(output_folder, "twilightgrey_combined_normalized_activity_profile.png")
plt.tight_layout()
plt.savefig(output_path)
plt.close()
