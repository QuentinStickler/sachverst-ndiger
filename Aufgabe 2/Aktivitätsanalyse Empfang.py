import os
import pandas as pd
import matplotlib.pyplot as plt

# Create a folder to store the images if it doesn't exist
output_folder = "received_messages_histograms"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Lade die CSV-Datei in ein DataFrame
data = pd.read_csv("Data.csv", sep="|", encoding="utf-16-LE")

# Remove leading and trailing spaces from the "Timestamp" string
data["Timestamp"] = data["Timestamp"].str.strip()

# Convert the "Timestamp" column to datetime format
data["Timestamp"] = pd.to_datetime(data["Timestamp"], utc=True)

# Extrahieren der Stundeninformation aus dem Zeitstempel
data["Hour"] = data["Timestamp"].dt.hour

# Group the data by "Recipient Names" and "Hour" and count the messages per hour
received_messages = data.groupby(["Recipient Name", "Hour"]).size().unstack(fill_value=0)

# Create histograms for the distribution of received messages for each user
for recipient_name, received_data in received_messages.iterrows():
    plt.figure(figsize=(10, 6))
    received_data.plot(kind="bar", color="skyblue")
    plt.title(f"Distribution of Received Messages for {recipient_name}")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Number of Received Messages")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    output_path = os.path.join(output_folder, f"{recipient_name}_received_messages_histogram.png")
    plt.savefig(output_path)  # Save the histogram as a PNG file in the specified folder
    plt.close()  # Close the current plot to free up memory