import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize

# Lade die CSV-Datei
data = pd.read_csv("python_output.csv", sep="|", encoding="utf-8")

# Gruppiere die Daten nach Sender Name
grouped_data = data.groupby("Sender Name")["Text"].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Tokenisiere die Nachrichten und erstelle einen Bag-of-Words-Vektor für jeden Nutzer
vectorizer = CountVectorizer(tokenizer=word_tokenize)
X = vectorizer.fit_transform(grouped_data["Text"])

# Berechne die Kosinusähnlichkeit zwischen den Nutzern
similarity_matrix = cosine_similarity(X)

# Erstelle ein DataFrame für die Ähnlichkeitsmatrix
similarity_df = pd.DataFrame(similarity_matrix, index=grouped_data["Sender Name"], columns=grouped_data["Sender Name"])

# Speichere die Ähnlichkeitsmatrix in einer CSV-Datei (optional)
similarity_df.to_csv("user_similarity_matrix.csv", encoding="utf-8")

# Extrahiere die Ähnlichkeiten in eine Liste von (Nutzer 1, Nutzer 2, Ähnlichkeit) Triplets
similarities = []
for i in range(len(similarity_df)):
    for j in range(i + 1, len(similarity_df)):  # Nur obere Dreiecksmatrix betrachten, um Duplikate zu vermeiden
        similarities.append((similarity_df.index[i], similarity_df.columns[j], similarity_df.iloc[i, j]))

# Sortiere die Ähnlichkeiten absteigend nach dem Ähnlichkeitswert
sorted_similarities = sorted(similarities, key=lambda x: x[2], reverse=True)

# Gib die Top-N-Nutzerpaare mit der größten Ähnlichkeit aus (z.B. die Top 10)
top_n = 30  # Anzahl der Paare, die angezeigt werden sollen
print(f"Top {top_n} Nutzerpaare mit der größten Ähnlichkeit:")
for i in range(top_n):
    user1, user2, similarity = sorted_similarities[i]
    print(f"{user1} und {user2} - Ähnlichkeit: {similarity:.4f}")

# Optional: Speichere die Top-N-Paare in einer CSV-Datei
output_file = "new_top_user_similarities.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("User 1,User 2,Similarity\n")
    for user1, user2, similarity in sorted_similarities[:top_n]:
        file.write(f"{user1},{user2},{similarity:.4f}\n")

print(f"Top {top_n} Nutzerpaare mit der größten Ähnlichkeit wurden in {output_file} gespeichert.")
