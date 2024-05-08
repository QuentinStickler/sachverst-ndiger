import pandas as pd

# Lade die CSV-Datei in ein DataFrame
data = pd.read_csv("Data.csv", sep="|", encoding="utf-16-LE")

# Remove leading and trailing spaces from the "Timestamp" string
data["Timestamp"] = data["Timestamp"].str.strip()

# Convert the "Timestamp" column to datetime format
data["Timestamp"] = pd.to_datetime(data["Timestamp"], utc=True)

# Extrahieren der Stundeninformation aus dem Zeitstempel
data["Hour"] = data["Timestamp"].dt.hour

# Group the data by "Sender Names" and "Hour" and count the messages per hour for senders
sender_activity_profiles = data.groupby(["Sender Name", "Hour"]).size().unstack(fill_value=0)

# Determine the preferred activity time of each sender
preferred_activity_time = sender_activity_profiles.idxmax(axis=1)

# Write the preferred activity time of each sender to a CSV file
preferred_activity_time.to_csv("preferred_activity_time.csv", header=["Preferred Activity Time"])

print("Preferred Activity Time of Each Sender has been saved to preferred_activity_time.csv")