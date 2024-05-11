import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
#nltk.download('punkt')

# Load the CSV file Data von Samsung SM-G950u1 Galaxy S8 TD-LTE
data_0 = pd.read_csv("Data Image 0.csv", sep="|", encoding="utf-16-LE")

# Encoding Error
#data_1 = pd.read_csv("Data Image 1.csv", sep="|", encoding="utf-16-LE")

# Daten anhand der Sender Namen gruppieren
# .apply(lambda x: ' '.join(map(str, x))): Diese Anweisung wendet eine Funktion auf jede Gruppe von Nachrichten an. 
# Die Funktion nimmt eine Liste von Nachrichten als Eingabe (x) und konvertiert sie in eine einzige Zeichenkette, indem sie join verwendet. 
# Zuerst wird jedoch map(str, x) aufgerufen, um sicherzustellen, dass alle Elemente in der Liste als Zeichenketten behandelt werden.
grouped_data = data_0.groupby("Sender Names")["Text"].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Erstellt die CSV Datei in dem das Ergebnis gespeichert wird in UTF 8 Encoding
output_file = "token_counts_data_1.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender,TokenCount\n")
    
    # Iteriert über alle Sender Nachrichten und tokenisiert sie
    for index, row in grouped_data.iterrows():
        sender_name = row["Sender Names"]
        sender_messages = row["Text"]
        
        # Tokenize the sender's messages
        tokens = word_tokenize(sender_messages)
        
        # Zählt die Anzahl jedes Tokens eines Senders
        token_counts = Counter(tokens)
        
         # Schreibt das Ergebnis in die Datei
        for token, count in token_counts.items():
            file.write(f"{sender_name},{token},{count}\n")

print(f"Token counts saved to {output_file}")