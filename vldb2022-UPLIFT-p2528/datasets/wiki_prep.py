import csv

# Input file path
input_file = 'wiki.en.vec'

# Output file paths
word_output_file = 'wiki_metaframe'
embedding_output_file = 'wiki_embeddings_csv'
word_list_file = 'wiki_words'

# Read embeddings from the input file
with open(input_file, 'r', encoding='utf-8') as infile:
    lines = infile.readlines()

# Extract metadata
metadata = lines[0].split()
num_rows = int(metadata[0])
embedding_dim = int(metadata[1])

# Extract words and embeddings
words = []
wordsOnly = []
seen = set()
embeddings = []
i = 1 

for line in lines[1:]:
    items = line.strip().split()
    word = items[0].strip('"') + '\u00b7' + str(i)
    word2 = items[0].strip('"')
    i = i + 1
    embedding = [float(val) for val in items[-300:]]
    words.append(word)
    embeddings.append(embedding)
    if word2 not in seen:
        seen.add(word2)
        wordsOnly.append(word2)

words.append('padword'+ '\u00b7' + str(num_rows+1));
pademd = [0.0 for i in range(embedding_dim)]
embeddings.append(pademd)

# Write words to CSV
with open(word_output_file, 'w', newline='', encoding='utf-8') as word_csv:
    writer = csv.writer(word_csv)
    writer.writerows(zip(words))

# Write only words to CSV. Need for Keras pipeline
with open(word_list_file, 'w', newline='', encoding='utf-8') as word_csv:
    writer = csv.writer(word_csv)
    writer.writerows(zip(wordsOnly))

# Write embeddings to CSV
with open(embedding_output_file, 'w', newline='', encoding='utf-8') as embedding_csv:
    writer = csv.writer(embedding_csv)
    writer.writerows(embeddings)

