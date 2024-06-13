import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import random
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# Load the CSV file
data = pd.read_csv("Data.csv", sep="|", encoding="utf-16-LE")

# Randomly select 10% of the data for labeling
random.seed(42)
sampled_data = data.sample(frac=0.1)

# Use the list of crime-related keywords to label the data
crime_keywords = ['heist', 'hit', 'job', 'score', 'boost', 'fence', 'knockover', 'run', 'scheme', 'racket', 'scam', 'grift', 'shakedown', 'smash and grab', 'clean', 'heat', 'lick', 'strap', 'piece', 'burner', 'chop shop', 'drop', 'hideout', 'stash', 'stakeout', 'inside man', 'mule', 'goon', 'muscle', 'snitch', 'rat', 'boss', 'capo', 'crew', 'outfit', 'connect', 'plug', 'trap house', 'turf', 'territory', 'hood', 'corner', 'deal', 'package', 'product', 'cook', 'cut', 'pure', 'bag', 'brick', 'key', 'pound', 'ounce', 'dime bag', 'nickel bag', 'rock', 'meth', 'heroin', 'blow', 'cocaine', 'weed', 'bud', 'smoke', 'joint', 'blunt', 'high', 'trip', 'fix', 'dope', 'junk', 'junkie', 'shooter', 'dealer', 'kingpin', 'cartel', 'gang', 'syndicate', 'mafia', 'mob', 'circle', 'clique', 'thug', 'pusher', 'supplier', 'source', 'ring', 'network', 'operation', 'fraud', 'con', 'hustle', 'swipe', 'lift', 'forge', 'fake', 'knockoff', 'launder', 'wash', 'clean', 'rip-off', 'jacker', 'mark', 'burner phone', 'hustle', 'skimmer', 'chop shop', 'hot goods', 'chop', 'clout', 'runner', 'spotter', 'lookout', 'hotwire', 'getaway', 'hijack', 'contraband', 'counterfeit', 'clip', 'crack', 'stash house', 'jack', 'score', 'break-in', 'smash', 'spray', 'getaway car', 'burner car', 'street value', 'backdoor', 'chop', 'deal', 'spot', 'corner', 'stash spot', 'drop-off', 'load', 'front', 'connect', 'supplier', 're-up', 'trap', 'plug', 'block', 'pound', 'zip', 'gram', 'ounce', 'baggie', 'dime', 'dub', 'cut', 'fix', 'hit', 'nod', 'bagman', 'mule', 'runner', 'drop', 'lookout', 'scoping', 'casing', 'watch', 'tail', 'shadow', 'stake', 'watch', 'heat', 'badge', 'blue', 'fuzz', 'five-o', 'narco', 'po-po', 'pig', 'flatfoot', 'copper', 'cuffs', 'cell', 'shank', 'solitary', 'lockdown', 'shiv', 'hooch', 'snitch', 'rat', 'stoolie', 'squealer', 'nark', 'grass', 'canary', 'squeak', 'fink', 'flip', 'informant', 'rat out', 'drop dime', 'talk', 'sing', 'chirp', 'roll over', 'testify', 'witness', 'blow the whistle', 'squeal', 'canary', 'whistleblower', 'grab', 'pop', 'clean out', 'knock off', 'burner', 'torch', 'bogus', 'dummy', 'phony', 'falsified', 'made up', 'tricked out', 'rigged', 'hooked', 'jacked up', 'scheme', 'setup', 'play', 'angle', 'extort', 'blackmail', 'threaten', 'lean on', 'squeeze', 'muscle', 'bully', 'pressure', 'intimidate', 'coerce', 'force', 'slot', 'lace', 'dose', 'spike', 'copied', 'pinch']

# Label the data based on the presence of crime-related keywords
sampled_data['Label'] = sampled_data['Text'].apply(lambda x: 1 if any(keyword in str(x).lower() for keyword in crime_keywords) else 0)

# Prepare the text data
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sampled_data['Text'].astype(str))
y = sampled_data['Label']

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train, y_train)

# Save the trained model and vectorizer
joblib.dump(model, 'crime_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')

# Load the model and vectorizer
model = joblib.load('crime_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

# Vectorize the full dataset
X_full = vectorizer.transform(data['Text'].astype(str))

# Predict the labels
data['Label'] = model.predict(X_full)

# Save the labeled CSV
data.to_csv('labeled_data.csv', sep='|', encoding='utf-16-LE', index=False)

# Filter the labeled data for criminal messages
criminal_messages = data[data['Label'] == 1]

# Save the filtered CSV
criminal_messages.to_csv('criminal_messages.csv', sep='|', encoding='utf-16-LE', index=False)