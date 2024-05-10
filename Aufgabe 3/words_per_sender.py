import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
#nltk.download('punkt')




# Load the CSV file
data_0 = pd.read_csv("Data Image 0.csv", sep="|", encoding="utf-16-LE")

# Group the data by sender names and aggregate the messages
grouped_data = data_0.groupby("Sender Names")["Text"].apply(lambda x: ' '.join(map(str, x))).reset_index()

# Create a file to write the token counts
output_file = "token_counts_data_0.csv"
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Sender,TokenCount\n")
    
    # Iterate over each sender's messages and tokenize them
    for index, row in grouped_data.iterrows():
        sender_name = row["Sender Names"]
        sender_messages = row["Text"]
        
        # Tokenize the sender's messages
        tokens = word_tokenize(sender_messages)
        
        # Count the tokens
        token_counts = Counter(tokens)
        
         # Write the sender name and token counts to the file
        for token, count in token_counts.items():
            file.write(f"{sender_name},{token},{count}\n")

print(f"Token counts saved to {output_file}")