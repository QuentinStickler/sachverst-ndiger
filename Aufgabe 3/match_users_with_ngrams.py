import pandas as pd
import nltk
from nltk.util import ngrams
from collections import Counter
from itertools import combinations

# nltk.download('punkt')

# Load the CSV file Data von Samsung SM-G950u1 Galaxy S8 TD-LTE
data = pd.read_csv("Data_Original.csv", sep="|", encoding="utf-16-LE")

# Daten anhand der Sender Namen gruppieren
grouped_data = data.groupby("Sender Name")["Text"].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Function to generate n-grams and their counts
def generate_ngrams(text, n):
    characters = list(text.replace(" ", ""))  # Remove spaces for character tokenization
    return Counter(ngrams(characters, n))

# Calculate n-grams for each sender and store them
ngram_data = {}
for index, row in grouped_data.iterrows():
    sender_name = row["Sender Name"]
    sender_messages = row["Text"]
    
    # Generate bigrams and trigrams
    bigrams = generate_ngrams(sender_messages, 2)
    trigrams = generate_ngrams(sender_messages, 3)
    
    # Combine bigrams and trigrams into one set
    ngram_data[sender_name] = bigrams + trigrams

# Function to calculate Jaccard similarity between two sets of n-grams
def jaccard_similarity(ngrams1, ngrams2):
    intersection = sum((ngrams1 & ngrams2).values())
    union = sum((ngrams1 | ngrams2).values())
    return intersection / union if union != 0 else 0

# Compare n-grams between all pairs of users
similarity_threshold = 0.5  # Define a threshold for similarity
potential_matches = []

for (sender1, ngrams1), (sender2, ngrams2) in combinations(ngram_data.items(), 2):
    similarity = jaccard_similarity(ngrams1, ngrams2)
    if similarity > similarity_threshold:
        potential_matches.append((sender1, sender2, similarity))

# Save potential matches to a CSV file
output_file = "potential_matches_ngrams.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender1,Sender2,Similarity\n")
    for sender1, sender2, similarity in potential_matches:
        file.write(f"{sender1},{sender2},{similarity:.2f}\n")

print(f"Potential matches saved to {output_file}")
