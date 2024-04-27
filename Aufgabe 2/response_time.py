import pandas as pd

# Load the CSV file into a DataFrame
data = pd.read_csv("Data.csv", sep="|", encoding="utf-16-LE")

# Remove leading and trailing spaces from the "Timestamp" string
data["Timestamp"] = data["Timestamp"].str.strip()

# Remove the UTC offset from the "Timestamp" string
data["Timestamp"] = data["Timestamp"].str.replace(" UTC[+-]\d{2}:\d{2}", "", regex=True)

# Convert the "Timestamp" column to datetime format
data["Timestamp"] = pd.to_datetime(data["Timestamp"], format="%d.%m.%Y %H:%M:%S")

# Sort the data by "Timestamp"
data = data.sort_values(by="Timestamp")

# Group the data by "Sender Names" and "Recipient Names" to calculate response times
response_times = data.groupby(["Sender Name", "Recipient Name"]).apply(lambda x: x["Timestamp"].diff())

# Calculate the average response time for each sender-recipient pair
average_response_times = response_times.groupby(["Sender Name", "Recipient Name"]).mean()

# Save the average response times to a CSV file
average_response_times.to_csv("average_response_times.csv", header=True)

print("Average Response Times have been saved to average_response_times.csv")
