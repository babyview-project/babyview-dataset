# Environment Setup & Packages

# Data Preprocessing

## Get Speaker Label Frequencies
`python preprocess_data/word_count_speaker_label_analysis.py`
`python preprocess_data/word_count_speaker_label_analysis_subfolders.py`

## Set Up Training Data
```
python scripts/preprocess_data/convert_conversation_csv_to_txt_files_remove_duplicates.py
python scripts/preprocess_data/convert_conversation_csv_to_txt_files_subfolders_remove_duplicates.py
python scripts/preprocess_data/get_train_val_txt_files.py {input_full_txt_file} {output_train_file} {output_val_file}
python scripts/preprocess_data/subsample_CHILDES_txt_files.py {input_full_txt_file} {output_subset_file} {total_words}
```
