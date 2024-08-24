import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from collections import Counter

nltk.download('punkt')

# Load the CSV file Data von Samsung SM-G950u1 Galaxy S8 TD-LTE
data = pd.read_csv("Data_Original.csv", sep="|", encoding="utf-16-LE")

# Daten anhand der Sender Namen gruppieren
grouped_data = data.groupby("Sender Name")["Text"].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Erstellt die CSV Datei in dem das Ergebnis gespeichert wird in UTF 8 Encoding
output_file = "bi_and_tri_counts_data.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender,TokenType,Token,Count\n")
    
    # Iteriert über alle Sender Nachrichten und tokenisiert sie
    for index, row in grouped_data.iterrows():
        sender_name = row["Sender Name"]
        sender_messages = row["Text"]
        
        # Tokenize the sender's messages into characters
        characters = list(sender_messages.replace(" ", ""))  # Entferne Leerzeichen für die Charakter-Tokenisierung
        
        # Erzeuge Bigrams und Trigrams
        bigrams = list(ngrams(characters, 2))
        trigrams = list(ngrams(characters, 3))
        
        # Zähle die Häufigkeit von Bigrams und Trigrams
        bigram_counts = Counter(bigrams)
        trigram_counts = Counter(trigrams)
        
        # Schreibt Bigram Ergebnisse in die Datei
        for bigram, count in bigram_counts.items():
            bigram_str = ''.join(bigram)
            file.write(f"{sender_name},Bigram,{bigram_str},{count}\n")
        
        # Schreibt Trigram Ergebnisse in die Datei
        for trigram, count in trigram_counts.items():
            trigram_str = ''.join(trigram)
            file.write(f"{sender_name},Trigram,{trigram_str},{count}\n")

print(f"Token counts saved to {output_file}")
