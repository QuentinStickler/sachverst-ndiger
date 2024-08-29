import pandas as pd
from nltk.util import ngrams
from collections import Counter
from itertools import combinations
import numpy as np

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

# Function to calculate Cosine similarity between two sets of n-grams
def cosine_similarity(ngrams1, ngrams2):
    # Get all unique n-grams
    all_ngrams = set(ngrams1.keys()).union(set(ngrams2.keys()))
    
    # Create vectors
    vec1 = np.array([ngrams1.get(ngram, 0) for ngram in all_ngrams])
    vec2 = np.array([ngrams2.get(ngram, 0) for ngram in all_ngrams])
    
    # Calculate cosine similarity
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2) if (norm1 != 0 and norm2 != 0) else 0

# Compare n-grams between all pairs of users
similarity_threshold = 0.5  # Define a threshold for similarity
potential_matches = []
seen_pairs = set()  # To keep track of already processed pairs

for (sender1, ngrams1), (sender2, ngrams2) in combinations(ngram_data.items(), 2):
    # Ensure each pair is only added once
    pair = tuple(sorted([sender1, sender2]))
    if pair not in seen_pairs:
        similarity = cosine_similarity(ngrams1, ngrams2)
        if similarity > similarity_threshold:
            potential_matches.append((sender1, sender2, similarity))
            seen_pairs.add(pair)

# Sort the list by similarity in descending order
potential_matches.sort(key=lambda x: x[2], reverse=True)

# Save potential matches to a CSV file
output_file = "potential_matches_cosine.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender1,Sender2,Similarity\n")
    for sender1, sender2, similarity in potential_matches:
        file.write(f"{sender1},{sender2},{similarity:.2f}\n")

print(f"Potential matches saved to {output_file}")

# Display the sorted list of similar sender pairs
print("Sorted list of sender pairs with high similarity:")
for sender1, sender2, similarity in potential_matches:
    print(f"Sender1: {sender1}, Sender2: {sender2}, Similarity: {similarity:.2f}")
