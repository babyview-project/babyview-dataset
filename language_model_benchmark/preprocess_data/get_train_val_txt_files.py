import random
import sys

input_file_path = sys.argv[1]
train_file_path = sys.argv[2]
val_file_path = sys.argv[3]

#input_file_path = 'data/babyview_all_convos.txt'
#train_file_path = 'data/train_data/babyview_train.txt'
#val_file_path = 'data/train_data/babyview_val.txt'

#input_file_path = 'data/saycam_all_convos.txt'
#train_file_path = 'data/train_data/saycam_train.txt'
#val_file_path = 'data/train_data/saycam_val.txt'

# Define the fraction of conversations to be used for validation
val_fraction = 0.15

# Read the combined conversations from the input file
with open(input_file_path, 'r') as input_file:
    conversations = input_file.readlines()

# Shuffle the conversations
random.seed(0)  # For reproducibility
random.shuffle(conversations)

# Calculate the number of validation samples
num_val_samples = int(len(conversations) * val_fraction)

# Split the conversations into train and val
val_conversations = conversations[:num_val_samples]
train_conversations = conversations[num_val_samples:]

# Write the validation conversations to the val file
with open(val_file_path, 'w') as val_file:
    val_file.writelines(val_conversations)

# Write the training conversations to the train file
with open(train_file_path, 'w') as train_file:
    train_file.writelines(train_conversations)

print(f"Train and validation files created successfully!")
print(f"Total conversations: {len(conversations)}")
print(f"Training conversations: {len(train_conversations)}")
print(f"Validation conversations: {len(val_conversations)}")

'''
Babyview:
Total conversations: 2776
Training conversations: 2360
Validation conversations: 416

Saycam:
Total conversations: 1910
Training conversations: 1624
Validation conversations: 286
'''

'''
Word counts of each file:

1624  2362676 13175128 data/train_data/saycam_train.txt
286   445110  2488270  data/train_data/saycam_val.txt

2360  2419541 13668863 data/train_data/babyview_train.txt
416   429875  2428744  data/train_data/babyview_val.txt

#Note: below combined files I manually combined by just pasting lines from both original files into new .txt files
3984  4782217 26843991 data/train_data/babyview_saycam_combined_train.txt
702   874985  4917014  data/train_data/babyview_saycam_combined_val.txt
'''