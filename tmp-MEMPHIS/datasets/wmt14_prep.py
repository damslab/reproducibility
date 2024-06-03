# https://nlp.stanford.edu/projects/nmt/

import csv
import string
import nltk
from nltk import word_tokenize
from langdetect import detect
nltk.download('punkt')

# Function to read the file and tokenize sentences
def tokenize_sentences(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    tokenized_sentences = [word_tokenize(sentence.strip()) for sentence in sentences]
    return tokenized_sentences

# Function to check if a word contains punctuation
def contains_punctuation(word):
    return any(char in string.punctuation for char in word)

# Function to check if a word contains numbers
def contains_numbers(word):
    return any(char.isdigit() for char in word)

# Function to check if a word is English using langdetect
def is_english(word):
    try:
        return detect(word) == 'en'
    except:
        # If an error occurs during language detection, assume the word is not English
        return False

# Function to write words into a CSV file
def write_to_csv(tokenized_sentences, output_file, skip_words, max_words):
    count = 0
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for sentence in tokenized_sentences:
            for word in sentence:
                if (not contains_punctuation(word) and not contains_numbers(word)
                        and (skip_words is None or word.lower() not in skip_words)):
                    csv_writer.writerow([word.lower()])
                    count += 1
                    if count >= max_words:
                        return

# File paths
input_file = '/home/arnab/datasets/WMT14_100k.en'
output_file = '/home/arnab/datasets/E2G_WMT14.csv'

# List of words to skip
skip_words = ['moodboard','pěveckých','vicenová']

# Tokenize sentences
tokenized_sentences = tokenize_sentences(input_file)

# Configurable token count 
max_words = 200000 
# Write words to CSV file
write_to_csv(tokenized_sentences, output_file, skip_words, max_words)

