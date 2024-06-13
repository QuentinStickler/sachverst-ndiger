import pandas as pd

data = pd.read_csv("Data.csv", sep="|", encoding="utf-16-LE")

from transformers import pipeline

# Load the pre-trained model for text classification
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# Function to classify messages
def classify_message(text):
    if pd.isna(text):
        return "Unknown"  # Handle missing or NaN values
    result = classifier(str(text))
    return result[0]['label']

# Apply the model to classify messages
data['Classification'] = data['Text'].apply(classify_message)

# Save the classified messages to a new CSV file
output_file = "classified_messages.csv"
data.to_csv(output_file, sep="|", encoding="utf-16-LE", index=False)

print(f"Classified messages saved to {output_file}")
