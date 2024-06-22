#same as the other script 'word_count_speaker_label_analysis.py', but this time assuming the .csv files are in different subfolders (as is the case with the babyview data)

import os
import pandas as pd
from collections import defaultdict

# Initialize counters
total_word_count = 0
total_utterances = 0
utterance_count = defaultdict(int)
num_files = 0
total_words_per_file = []
total_utterances_per_file = []

# Define the root folder containing the subfolders with .csv files
root_folder_path = 'data/babyview_data'

# Loop through all subfolders and CSV files
for subdir, _, files in os.walk(root_folder_path):
    for filename in files:
        if filename.endswith('.csv'):
            # Read the CSV file into a DataFrame
            file_path = os.path.join(subdir, filename)
            df = pd.read_csv(file_path)
            
            # Increment the file counter
            num_files += 1
            
            # Initialize counters for the current file
            file_word_count = 0
            file_utterance_count = 0

            # Calculate the total word count and utterance count for the current file
            for text in df['text']:
                word_count = len(str(text).split())
                file_word_count += word_count
                total_word_count += word_count
            
            file_utterance_count = len(df)
            total_utterances += file_utterance_count
            
            # Append counts to lists for averaging later
            total_words_per_file.append(file_word_count)
            total_utterances_per_file.append(file_utterance_count)

            # Count the total number of utterances each speaker label occurs for
            for speaker in df['speaker']:
                utterance_count[speaker] += 1

# Calculate the fraction of utterances that have each speaker label
speaker_fractions = {speaker: count / total_utterances for speaker, count in utterance_count.items()}

# Calculate the average number of utterances and words per file
average_utterances_per_file = total_utterances / num_files
average_words_per_file = total_word_count / num_files

# Output the results
print(f"Total word count of all utterances combined: {total_word_count}")
print(f"Total number of utterances: {total_utterances}")
print(f"Number of conversations (CSV files): {num_files}")
print(f"Average number of utterances per conversation: {average_utterances_per_file:.2f}")
print(f"Average number of words per conversation: {average_words_per_file:.2f}")

print("Total number of utterances for each speaker label:")
for speaker, count in utterance_count.items():
    print(f"{speaker}: {count}")
print("Fraction of utterances for each speaker label:")
for speaker, fraction in speaker_fractions.items():
    print(f"{speaker}: {fraction:.2%}")

'''
Babyview data:

Total word count of all utterances combined: 2323525
Total number of utterances: 514088
Number of conversations (CSV files): 3138
Average number of utterances per conversation: 163.83
Average number of words per conversation: 740.45

Total number of utterances for each speaker label:
FEM: 196971
KCHI: 105801
MAL: 100056
CHI: 55884
nan: 55349

Fraction of utterances for each speaker label:
FEM: 38.31%
KCHI: 20.58%
MAL: 19.46%
CHI: 10.87%
nan: 10.77%
'''