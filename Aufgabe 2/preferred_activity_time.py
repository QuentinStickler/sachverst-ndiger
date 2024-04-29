import pandas as pd

# Lade die CSV-Datei in ein DataFrame
data = pd.read_csv("Data.csv", sep="|", encoding="utf-16-LE")

# Remove leading and trailing spaces from the "Timestamp" string
data["Timestamp"] = data["Timestamp"].str.strip()

# Remove the UTC offset from the "Timestamp" string
data["Timestamp"] = data["Timestamp"].str.replace(" UTC[+-]\d{2}:\d{2}", "", regex=True)

# Convert the "Timestamp" column to datetime format
data["Timestamp"] = pd.to_datetime(data["Timestamp"], format="%d.%m.%Y %H:%M:%S")

# Extrahieren der Stundeninformation aus dem Zeitstempel
data["Hour"] = data["Timestamp"].dt.hour

# Group the data by "Sender Names" and "Hour" and count the messages per hour for senders
sender_activity_profiles = data.groupby(["Sender Name", "Hour"]).size().unstack(fill_value=0)

# Determine the preferred activity time of each sender
preferred_activity_time = sender_activity_profiles.idxmax(axis=1)

# Write the preferred activity time of each sender to a CSV file
preferred_activity_time.to_csv("preferred_activity_time.csv", header=["Preferred Activity Time"])

print("Preferred Activity Time of Each Sender has been saved to preferred_activity_time.csv")