export TRAIN_FILE=$1
export TEST_FILE=$2
export TOKENIZER_FOLDER=$3
export CONFIG_FOLDER=$4
export MODEL_DIR=$5 

export MODEL_TYPE="gpt2" #gpt2 #This is the specific arch
export MODEL_SIZE=$6 #This is the specific arch you want to use within this type e.g roberta-base, roberta-large, etc.

export LR=$7
export NUM_TRAIN_EPOCHS=$8
export PER_GPU_TRAIN_BATCH_SIZE=$9
export SEED=42

echo $LR
echo $MODEL_SIZE
echo $NUM_TRAIN_EPOCHS
echo $PER_GPU_TRAIN_BATCH_SIZE

CUDA_VISIBLE_DEVICES=0,1,2,3 python3 language_model_training/run_clm.py \
	--model_type ${MODEL_SIZE} \
	--config_name ${CONFIG_FOLDER} \
	--tokenizer_name ${TOKENIZER_FOLDER} \
    --train_file ${TRAIN_FILE} \
    --validation_file ${TEST_FILE} \
	--keep_linebreaks True \
    --per_device_train_batch_size ${PER_GPU_TRAIN_BATCH_SIZE} \
    --per_device_eval_batch_size ${PER_GPU_TRAIN_BATCH_SIZE} \
    --do_train \
    --do_eval \
    --output_dir ${MODEL_DIR} \
	--seed ${SEED} \
    --learning_rate ${LR} \
    --num_train_epochs ${NUM_TRAIN_EPOCHS} \
	--load_best_model_at_end \
	--evaluation_strategy 'epoch' \
	--save_strategy 'epoch' \
    --save_total_limit 2 \
	--logging_steps 10