import os
import pandas as pd
import matplotlib.pyplot as plt


# Create a folder to store the images if it doesn't exist
output_folder = "activity_profiles_images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

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

# Group the data by "Sender Names" (case-sensitive) and "Hour" and count the messages per hour
activity_profile = data.groupby([data["Sender Name"].str.strip(), "Hour"]).size().unstack(fill_value=0)

# Create histograms for each user's activity profile
for sender_name in activity_profile.index:
    plt.figure(figsize=(10, 6))
    activity_profile.loc[sender_name].plot(kind="bar", color="skyblue")
    plt.title(f"Activity Profile for {sender_name}")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Messages")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    output_path = os.path.join(output_folder, f"{sender_name}_activity_profile.png")
    plt.savefig(output_path)  # Save the histogram as a PNG file in the specified folder
    plt.close()  # Close the current plot to free up memory