#same as the other script 'convert_conversation_csv_to_txt_files_remove_duplicates.py', but this time assuming the .csv files are in different subfolders (as is the case with the babyview data)

import os
import pandas as pd

# Define the root folder containing the subfolders with .csv files
root_folder_path = 'data/babyview_data'

# Define the output file path
output_file_path = 'data/babyview_all_convos.txt'

# Define the approximate total number of words
X = 2000000

# Speaker label replacements
speaker_replacements = {'KCHI': 'CHI', 'FEM': 'MOT', 'CHI': 'OCHI'}

# Initialize variables
all_conversations = set()  # Use a set to avoid duplicate conversations
current_word_count = 0

def remove_consecutive_duplicates(df):
    """Remove consecutive duplicate rows with the same 'text' and 'speaker'."""
    df['duplicate'] = (df['text'] == df['text'].shift()) & (df['speaker'] == df['speaker'].shift())
    df = df[~df['duplicate']]
    return df.drop(columns=['duplicate'])

# Loop through all subfolders and CSV files
for subdir, _, files in os.walk(root_folder_path):
    for filename in files:
        if filename.endswith('.csv'):
            # Read the CSV file into a DataFrame
            file_path = os.path.join(subdir, filename)
            df = pd.read_csv(file_path, na_filter=False)
            
            # Remove consecutive duplicate lines
            df = remove_consecutive_duplicates(df)
            
            # Sort the DataFrame by utterance number
            df = df.sort_values('utterance_no')
            
            # Build the conversation string
            conversation = []
            conversation_word_count = 0
            for _, row in df.iterrows():
                speaker = speaker_replacements.get(row['speaker'], row['speaker'])
                text = row['text']
                conversation.append(f"**{speaker}**: {text}")
                conversation_word_count += len(str(text).split())
            
            # Convert the list to a string
            conversation_str = " \\n\\n ".join(conversation) + " <|endoftext|>\n"
            
            # Add conversation to the set if it doesn't exceed the word limit and is not a duplicate
            if current_word_count + conversation_word_count <= X and conversation_str not in all_conversations:
                all_conversations.add(conversation_str)
                current_word_count += conversation_word_count
            if current_word_count >= X:
                break

# Write all conversations to the output file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(all_conversations)

print(f"Combined conversations file created successfully with {current_word_count} words!")

'''
output of wc data/babyview_all_convos.txt:
2776  2849416 16097607 data/babyview_all_convos.txt
'''