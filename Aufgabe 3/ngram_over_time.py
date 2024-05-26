import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter
from datetime import datetime

# Download NLTK data
nltk.download('punkt')

# Function to generate n-grams from a list of tokens
def generate_ngrams(tokens, n):
    return list(ngrams(tokens, n))

# Load the CSV file
data_0 = pd.read_csv("Data Image 0.csv", sep="|", encoding="utf-16-LE")

# Remove leading and trailing spaces from the "Timestamp" string
data_0["Timestamp"] = data_0["Timestamp"].str.strip()

# Convert the "Timestamp" column to datetime format
data_0["Timestamp"] = pd.to_datetime(data_0["Timestamp"], utc=True)

# Create a file to write the n-grams
output_file = "ngrams_overtime.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender;Date;Ngram;Count\n")
    
    # Iterate over each sender's messages
    for sender_name, group in data_0.groupby("Sender Names"):
        # Sort messages by timestamp
        group = group.sort_values(by='Timestamp')
        
        # Iterate over each date
        for date, messages_on_date in group.groupby(group['Timestamp'].dt.date):
            # Concatenate all messages on that date
            messages = ' '.join(map(str, messages_on_date['Text']))
            
            # Tokenize the messages
            tokens = word_tokenize(messages)
            
            # Generate n-grams
            n = 3  # Change n to the desired value for n-grams
            date_ngrams = generate_ngrams(tokens, n)
            
            # Count the n-grams
            ngram_counts = Counter(date_ngrams)
            
            # Write the sender name, date, and n-gram counts to the file
            for ngram, count in ngram_counts.items():
                ngram_str = ' '.join(ngram)  # Convert tuple to string
                file.write(f"{sender_name};{date};{ngram_str};{count}\n")

print(f"N-grams over time saved to {output_file}")
