import csv

search_words = ['gear', 'money', '$', 'packet', 'parcel', 'delivery', 'today', 'tomorrow', 'shit']

def contains_search_word(row, search_words):
    return any(word in ' '.join(row) for word in search_words)

#Filter input .csv file
def filter_csv(input_file, output_file, search_words):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        
        filtered_rows = [headers]
        
        for row in reader:
            if contains_search_word(row, search_words):
                filtered_rows.append(row)
                
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(filtered_rows)

input_csv = r'A:\HSMW\2. Semester\Sachverständiger\sachverst-ndiger\ngrams_overtime.csv' 
output_csv = 'caserelevantmessages.csv' 

filter_csv(input_csv, output_csv, search_words)
