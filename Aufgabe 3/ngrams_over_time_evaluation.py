import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the CSV file into a DataFrame
file_path = 'new_word_trigrams_overtime_all_data.csv'
df = pd.read_csv(file_path, delimiter='|')

# Step 2: Group by Date and Ngram
# Group by Date and Ngram to identify common n-grams shared by different senders on the same date
grouped = df.groupby(['Date', 'Ngram'])['Sender'].apply(list).reset_index()

# Step 3: Create a Sender-to-Ngram Matrix
# Initialize a dictionary to store n-gram counts for each sender
sender_ngrams = {}
for _, row in grouped.iterrows():
    ngram = row['Ngram']
    senders = row['Sender']
    for sender in senders:
        if sender not in sender_ngrams:
            sender_ngrams[sender] = []
        sender_ngrams[sender].append(ngram)

# Convert the sender_ngrams dictionary to a DataFrame
sender_df = pd.DataFrame(list(sender_ngrams.items()), columns=['Sender', 'Ngrams'])

# Convert the list of n-grams for each sender into a string for vectorization
sender_df['Ngram_String'] = sender_df['Ngrams'].apply(lambda x: ' '.join(x))

# Use CountVectorizer to create a matrix of n-gram counts
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sender_df['Ngram_String'])

# Step 4: Calculate Cosine Similarity Matrix
cosine_sim = cosine_similarity(X)

# Convert the cosine similarity matrix to a DataFrame
cosine_sim_df = pd.DataFrame(cosine_sim, index=sender_df['Sender'], columns=sender_df['Sender'])

# Step 5: Create a List of Sender Pairs with Similarity Scores
similarity_list = []
seen_pairs = set()  # To keep track of already processed pairs

# Iterate over the cosine similarity matrix and store the results
for sender1 in cosine_sim_df.index:
    for sender2 in cosine_sim_df.columns:
        if sender1 != sender2:
            # Ensure each pair is only added once
            pair = tuple(sorted([sender1, sender2]))
            if pair not in seen_pairs:
                similarity = cosine_sim_df.at[sender1, sender2]
                if similarity > 0.5:  # Define a threshold for "high similarity"
                    similarity_list.append((sender1, sender2, similarity))
                    seen_pairs.add(pair)

# Sort the list by similarity in descending order
similarity_list.sort(key=lambda x: x[2], reverse=True)

# Optionally, save the list to a CSV file
output_path = 'new_sorted_sender_similarity_list_trigrams.csv'
with open(output_path, 'w', encoding='utf-8') as file:
    file.write("Sender1,Sender2,Similarity\n")
    for sender1, sender2, similarity in similarity_list:
        file.write(f"{sender1},{sender2},{similarity:.4f}\n")

print("Sorted sender similarity list saved to", output_path)

# Display the sorted list of similar sender pairs
#print("List of sender pairs with high similarity (sorted):")
#for sender1, sender2, similarity in similarity_list:
#    print(f"Sender1: {sender1}, Sender2: {sender2}, Similarity: {similarity:.4f}")
