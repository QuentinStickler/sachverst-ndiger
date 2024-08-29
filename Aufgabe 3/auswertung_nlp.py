import pandas as pd

# Laden der klassifizierten Nachrichten
data = pd.read_csv("new_classified_messages.csv", sep="|", encoding="utf-8")

# Statistiken über die Klassifikationen
classification_counts = data['Classification'].value_counts()
total_messages = len(data)

print("Statistik der Klassifikationen:")
print(classification_counts)

# Prozentualer Anteil jeder Klassifikation
classification_percentages = (classification_counts / total_messages) * 100

print("\nProzentualer Anteil jeder Klassifikation:")
print(classification_percentages)

# Durchschnittliche Länge der Nachrichten pro Klassifikation (optional)
data['Text_Length'] = data['Text'].apply(lambda x: len(str(x)) if pd.notna(x) else 0)
average_length_per_classification = data.groupby('Classification')['Text_Length'].mean()

print("\nDurchschnittliche Länge der Nachrichten pro Klassifikation:")
print(average_length_per_classification)

# Berechnung der relativen Häufigkeiten (Prozentsätze) pro Sender und Klassifikation
sender_classification_counts = data.groupby(['Sender Name', 'Classification']).size()
sender_total_counts = data.groupby('Sender Name').size()
sender_classification_percentages = (sender_classification_counts / sender_total_counts) * 100

# Umwandeln in ein DataFrame
sender_classification_percentages_df = sender_classification_percentages.reset_index(name='Percentage')

# Sortieren nach den Prozentsätzen (absteigend)
sorted_sender_classification_percentages_df = sender_classification_percentages_df.sort_values(by='Percentage', ascending=False)

# Ausgabe der sortierten relativen Häufigkeiten für "POSITIVE" Nachrichten (sofern "POSITIVE" eine der Kategorien ist)
if 'POSITIVE' in data['Classification'].unique():
    positive_senders_percentage = sorted_sender_classification_percentages_df[sorted_sender_classification_percentages_df['Classification'] == 'POSITIVE']
    print("\nSortierte relative Häufigkeiten der positiven Nachrichten je Sender:")
    print(positive_senders_percentage)

# Ausgabe der sortierten relativen Häufigkeiten für "NEGATIVE" Nachrichten (sofern "NEGATIVE" eine der Kategorien ist)
if 'NEGATIVE' in data['Classification'].unique():
    negative_senders_percentage = sorted_sender_classification_percentages_df[sorted_sender_classification_percentages_df['Classification'] == 'NEGATIVE']
    print("\nSortierte relative Häufigkeiten der negativen Nachrichten je Sender:")
    print(negative_senders_percentage)

# Speichern der sortierten relativen Häufigkeiten in einer neuen CSV-Datei
percentage_output_file = "new_sorted_sender_classification_percentages.csv"
sorted_sender_classification_percentages_df.to_csv(percentage_output_file, sep="|", encoding="utf-16-LE", index=False)

print(f"\nDie sortierten relativen Häufigkeiten wurden in {percentage_output_file} gespeichert.")
