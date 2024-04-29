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

# Get list of all senders
senders = sender_activity_profiles.index

# Create an empty dictionary to store correlations between senders
sender_correlations = {}

# Calculate correlations between activity profiles of each pair of senders
for sender1 in senders:
    for sender2 in senders:
        if sender1 != sender2:
            correlation = sender_activity_profiles.loc[sender1].corr(sender_activity_profiles.loc[sender2])
            sender_correlations[(sender1, sender2)] = correlation

# Convert dictionary to DataFrame
sender_correlation_df = pd.DataFrame(sender_correlations, index=["Correlation"]).T

# Save the correlation results to a CSV file
sender_correlation_df.to_csv("sender_correlation_results.csv")

print("Correlation Between Different Senders Based on Activity Time has been saved to sender_correlation_results.csv")

# Filter correlation DataFrame for correlations higher than 0.8
high_correlation_df = sender_correlation_df[sender_correlation_df["Correlation"] > 0.8]

# Save the high correlation results to a CSV file
high_correlation_df.to_csv("high_correlation_results.csv")

print("Sender pairs with correlation higher than 0.8 have been saved to high_correlation_results.csv")