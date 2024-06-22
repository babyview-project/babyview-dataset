#! pip install tokenizers
import sys

train_file = sys.argv[1]
val_file = sys.argv[2]
tokenizer_path = sys.argv[3]

paths = [train_file,val_file]
#paths = ['data/train_data/babyview_train.txt','data/train_data/babyview_val.txt'] #Babyview
#paths = ['data/train_data/saycam_train.txt','data/train_data/saycam_val.txt'] #Saycam
#paths = ['data/train_data/babyview_saycam_combined_train.txt','data/train_data/babyview_saycam_combined_val.txt'] #Babyview + Saycam combined
#paths = ['data/train_data/CHILDES_2m_subset_train.txt','data/train_data/CHILDES_2m_subset_val.txt'] #CHILDES_2m
#paths = ['data/train_data/CHILDES_4m_subset_train.txt','data/train_data/CHILDES_4m_subset_val.txt'] #CHILDES_4m

from transformers import AutoTokenizer
old_tokenizer = AutoTokenizer.from_pretrained("gpt2")

#Add <UNK> special token into the vocab
special_token = '<UNK>'
#old_tokenizer.add_tokens([special_token])
special_tokens_dict = {'additional_special_tokens': ['<UNK>']}
old_tokenizer.add_special_tokens(special_tokens_dict)


example = '''def add_numbers(a, b):
    """Add the two numbers `a` and `b`."""
    return a + b'''

tokens = old_tokenizer.tokenize(example)
print(tokens)


def get_training_corpus(raw_dataset):
    return (
        raw_dataset[i : i + 1000]
        for i in range(0, len(raw_dataset), 1000)
    )

lines = []
for fn in paths:
    f = open(fn,'r')
    lines.extend(f.readlines())
print(len(lines))

CHILDES_corpus = get_training_corpus(lines)

tokenizer = old_tokenizer.train_new_from_iterator(CHILDES_corpus, 52000)

tokenizer.save_pretrained(tokenizer_path)
#tokenizer.save_pretrained("tokenizers/GPT2_babyview") #Babyview
#tokenizer.save_pretrained("tokenizers/GPT2_saycam") #Saycam
#tokenizer.save_pretrained("tokenizers/GPT2_babyview_saycam_combined") #Babyview + Saycam combined
#tokenizer.save_pretrained("tokenizers/GPT2_CHILDES_2m") #CHILDES_2m
#tokenizer.save_pretrained("tokenizers/GPT2_CHILDES_4m") #CHILDES_4m

# Print all special tokens
print("All special tokens:", tokenizer.all_special_tokens)

# Print individual special tokens
print("BOS token:", tokenizer.bos_token)
print("EOS token:", tokenizer.eos_token)
print("PAD token:", tokenizer.pad_token)
print("UNK token:", tokenizer.unk_token)
print("SEP token:", tokenizer.sep_token)
print("CLS token:", tokenizer.cls_token)
print("MASK token:", tokenizer.mask_token)