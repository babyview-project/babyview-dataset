import random

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
total_words = int(sys.argv[3])

# Train split

#input_file_path = '../CHILDES/train_data/CHILDES_train_randomized.txt'
#output_file_path = 'data/train_data/CHILDES_2m_subset_train.txt'
#total_words = 2400000 #for train, to match total number of words in saycam and babyview

#input_file_path = '../CHILDES/train_data/CHILDES_train_randomized.txt'
#output_file_path = 'data/train_data/CHILDES_4m_subset_train.txt'
#total_words = 4800000 #for train, to match total number of words in saycam plus babyview

# Val split

#input_file_path = '../CHILDES/train_data/CHILDES_val_randomized.txt'
#output_file_path = 'data/train_data/CHILDES_2m_subset_val.txt'
#total_words = 440000 #for val, to match total number of words in saycam and babyview

#input_file_path = '../CHILDES/train_data/CHILDES_val_randomized.txt'
#output_file_path = 'data/train_data/CHILDES_4m_subset_val.txt'
#total_words = 880000 #for val, to match total number of words in saycam plus babyview


# Read the large conversations file
with open(input_file_path, 'r') as input_file:
    conversations = input_file.readlines()

# Shuffle the conversations
random.seed(0)  # For reproducibility
random.shuffle(conversations)

# Initialize variables
current_word_count = 0
selected_conversations = []

# Function to count words in a conversation
def count_words(conversation):
    return len(conversation.split())

# Select conversations until the word count is approximately total_words
for conversation in conversations:
    word_count = count_words(conversation)
    if current_word_count + word_count <= total_words:
        selected_conversations.append(conversation)
        current_word_count += word_count
    else:
        break

# Write the selected conversations to the output file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(selected_conversations)

print(f"Subsampled CHILDES conversations file created successfully with approximately {current_word_count} words!")

#2m train: 2392788 words
#    942  2392788 13420351 data/train_data/CHILDES_2m_subset_train.txt
#2m val: 439643 words
#   177  439643 2475134 data/train_data/CHILDES_2m_subset_val.txt
#4m train: 4798530 words
#   1894  4798530 26932924 data/train_data/CHILDES_4m_subset_train.txt
#4m val: 875263 words
#   347  875263 4924072 data/train_data/CHILDES_4m_subset_val.txt