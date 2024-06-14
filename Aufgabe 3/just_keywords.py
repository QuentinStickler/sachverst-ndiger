import pandas as pd

# Define crime-related keywords
crime_keywords = ['heist', 'hit', 'job', 'score', 'boost', 'fence', 'knockover', 'run', 'scheme', 'racket', 'scam', 'grift', 'shakedown', 'smash and grab', 'clean', 'heat', 'lick', 'strap', 'piece', 'burner', 'chop shop', 'drop', 'hideout', 'stash', 'stakeout', 'inside man', 'mule', 'goon', 'muscle', 'snitch', 'rat', 'boss', 'capo', 'crew', 'outfit', 'connect', 'plug', 'trap house', 'turf', 'territory', 'hood', 'corner', 'deal', 'package', 'product', 'cook', 'cut', 'pure', 'bag', 'brick', 'key', 'pound', 'ounce', 'dime bag', 'nickel bag', 'rock', 'meth', 'heroin', 'blow', 'cocaine', 'weed', 'bud', 'smoke', 'joint', 'blunt', 'high', 'trip', 'fix', 'dope', 'junk', 'junkie', 'shooter', 'dealer', 'kingpin', 'cartel', 'gang', 'syndicate', 'mafia', 'mob', 'circle', 'clique', 'thug', 'pusher', 'supplier', 'source', 'ring', 'network', 'operation', 'fraud', 'con', 'hustle', 'swipe', 'lift', 'forge', 'fake', 'knockoff', 'launder', 'wash', 'clean', 'rip-off', 'jacker', 'mark', 'burner phone', 'hustle', 'skimmer', 'chop shop', 'hot goods', 'chop', 'clout', 'runner', 'spotter', 'lookout', 'hotwire', 'getaway', 'hijack', 'contraband', 'counterfeit', 'clip', 'crack', 'stash house', 'jack', 'score', 'break-in', 'smash', 'spray', 'getaway car', 'burner car', 'street value', 'backdoor', 'chop', 'deal', 'spot', 'corner', 'stash spot', 'drop-off', 'load', 'front', 'connect', 'supplier', 're-up', 'trap', 'plug', 'block', 'pound', 'zip', 'gram', 'ounce', 'baggie', 'dime', 'dub', 'cut', 'fix', 'hit', 'nod', 'bagman', 'mule', 'runner', 'drop', 'lookout', 'scoping', 'casing', 'watch', 'tail', 'shadow', 'stake', 'watch', 'heat', 'badge', 'blue', 'fuzz', 'five-o', 'narco', 'po-po', 'pig', 'flatfoot', 'copper', 'cuffs', 'cell', 'shank', 'solitary', 'lockdown', 'shiv', 'hooch', 'snitch', 'rat', 'stoolie', 'squealer', 'nark', 'grass', 'canary', 'squeak', 'fink', 'flip', 'informant', 'rat out', 'drop dime', 'talk', 'sing', 'chirp', 'roll over', 'testify', 'witness', 'blow the whistle', 'squeal', 'canary', 'whistleblower', 'grab', 'pop', 'clean out', 'knock off', 'burner', 'torch', 'bogus', 'dummy', 'phony', 'falsified', 'made up', 'tricked out', 'rigged', 'hooked', 'jacked up', 'scheme', 'setup', 'play', 'angle', 'extort', 'blackmail', 'threaten', 'lean on', 'squeeze', 'muscle', 'bully', 'pressure', 'intimidate', 'coerce', 'force', 'slot', 'lace', 'dose', 'spike', 'copied', 'pinch']

# Load the CSV file
data = pd.read_csv("Data.csv", sep="|", encoding="utf-16-LE")

# Filter messages containing any of the crime-related keywords
def contains_crime_keywords(text):
    text = str(text).lower()
    return any(keyword in text for keyword in crime_keywords)

filtered_data = data[data['Text'].apply(contains_crime_keywords)]

# Save the filtered messages to a new CSV file
filtered_data.to_csv('filtered_criminal_messages.csv', sep='|', encoding='utf-16-LE', index=False)
