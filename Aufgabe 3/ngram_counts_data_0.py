import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter

# Download NLTK data
# nltk.download('punkt')

# Function to generate n-grams from a list of tokens
def generate_ngrams(tokens, n):
    return list(ngrams(tokens, n))

# Load the CSV file
data_0 = pd.read_csv("Data Image 0.csv", sep="|", encoding="utf-16-LE")

# Group the data by sender names and aggregate the messages
grouped_data = data_0.groupby("Sender Names")["Text"].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Create a file to write the n-grams
output_file = "trigrams_data_0.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender;Ngram;Count\n")
    
    # Iterate over each sender's messages and generate n-grams
    for index, row in grouped_data.iterrows():
        sender_name = row["Sender Names"]
        sender_messages = row["Text"]
        
        # Tokenize the sender's messages
        tokens = word_tokenize(sender_messages)
        
        # Generate n-grams
        n = 3  # Change n to the desired value for n-grams
        sender_ngrams = generate_ngrams(tokens, n)
        #sender_ngrams = generate_ngrams(sender_messages, n)
        
        # Count the n-grams
        ngram_counts = Counter(sender_ngrams)
        
        # Write the sender name and n-gram counts to the file
        for ngram, count in ngram_counts.items():
            file.write(f"{sender_name};{ngram};{count}\n")

print(f"N-grams saved to {output_file}")
