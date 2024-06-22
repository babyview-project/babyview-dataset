# Environment Setup & Packages
TBD

# Data Preprocessing

## Get Speaker Label Frequencies
```
python preprocess_data/word_count_speaker_label_analysis.py
python preprocess_data/word_count_speaker_label_analysis_subfolders.py
```

## Set Up Training Data
```
python preprocess_data/convert_conversation_csv_to_txt_files_remove_duplicates.py
python preprocess_data/convert_conversation_csv_to_txt_files_subfolders_remove_duplicates.py
python preprocess_data/get_train_val_txt_files.py {input_full_txt_file} {output_train_file} {output_val_file}
python preprocess_data/subsample_CHILDES_txt_files.py {input_full_txt_file} {output_subset_file} {total_words}
```

# GPT-2 Training

## Tokenizer Training
```
python tokenizers/train_GPT2_tokenizer.py {train_txt_file} {val_txt_file} {tokenizer_path}
python tokenizers/test_GPT2_tokenizers.py
```

## Model Training
Note: model training scripts from HuggingFace Transformers for Causal LM training, with slight modifications. Links: TBD
```
bash language_model_training/finetune_generator_GPT2_CHILDES_multiple-epochs_4-GPUs.sh {train_txt_file} {val_txt_file} {tokenizer_path} tokenizers/GPT2-small_config {model_output_path} gpt2 {learning_rate} {num_epochs} {per_device_batch_size}
```

Example command:
`bash language_model_training/finetune_generator_GPT2_CHILDES_multiple-epochs_4-GPUs.sh data/train_data/babyview_train.txt data/train_data/babyview_val.txt tokenizers/GPT2_babyview tokenizers/GPT2-small_config trained_GPT2_models/GPT2-small_babyview_1e-04_20-epochs gpt2 1e-04 20 16`

# Zorro Evaluation
Note: Zorro data from original Zorro GitHub repo, and evaluation using the BabyLM BLIMP evaluation pipeline. Links: TBD

## Data Preprocessing
```
python zorro_evaluation/zorro_to_blimp.py
python zorro_evaluation/convert_zorro_to_dialogue_format_newlines_CHILDES.py {speaker_label}
```

## Run Evaluation
```
python babylm_eval_zorro.py {model_path} 'decoder' {zorro, zorro_dialogue-format-CHILDES_CHI, zorro_dialogue-format-CHILDES_MOT}
```
TBD: explain Zorro eval process in detail
