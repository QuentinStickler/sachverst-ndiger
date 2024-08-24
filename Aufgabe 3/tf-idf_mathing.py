import pandas as pd
import nltk
from nltk.util import ngrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations

# nltk.download('punkt')

# Load the CSV file Data von Samsung SM-G950u1 Galaxy S8 TD-LTE
data = pd.read_csv("Data_Original.csv", sep="|", encoding="utf-16-LE")

# Daten anhand der Sender Namen gruppieren
grouped_data = data.groupby("Sender Name")["Text"].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Function to generate character n-grams from text
def generate_ngrams(text, n):
    characters = list(text.replace(" ", ""))  # Remove spaces for character tokenization
    ngrams_list = [''.join(gram) for gram in ngrams(characters, n)]
    return ' '.join(ngrams_list)

# Combine all n-grams (bigrams and trigrams) for each user into a single string
grouped_data['Bigrams'] = grouped_data['Text'].apply(lambda x: generate_ngrams(x, 2))
grouped_data['Trigrams'] = grouped_data['Text'].apply(lambda x: generate_ngrams(x, 3))
grouped_data['AllNgrams'] = grouped_data['Bigrams'] + ' ' + grouped_data['Trigrams']

# Calculate TF-IDF for the n-grams of all users
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(grouped_data['AllNgrams'])

# Calculate cosine similarity between all pairs of users
cosine_sim = cosine_similarity(tfidf_matrix)

# Identify potential matches based on cosine similarity
similarity_threshold = 0.5  # Define a threshold for similarity
potential_matches = []

for i, j in combinations(range(len(grouped_data)), 2):
    if cosine_sim[i, j] > similarity_threshold:
        potential_matches.append((grouped_data.iloc[i]['Sender Name'], grouped_data.iloc[j]['Sender Name'], cosine_sim[i, j]))

# Save potential matches to a CSV file
output_file = "potential_matches_tfidf.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender1,Sender2,Similarity\n")
    for sender1, sender2, similarity in potential_matches:
        file.write(f"{sender1},{sender2},{similarity:.2f}\n")

print(f"Potential matches saved to {output_file}")
