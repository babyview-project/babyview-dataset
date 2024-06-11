# %%
import os
import pandas as pd
from glob import glob

url_base = "http://localhost:8888"
csv_file_name = "./to_sample_for_whisper.csv"
df = pd.read_csv(csv_file_name)

# %% extract all frames
dataset_root_path = "/data/yinzi/babyview_20240507/"
tmp_frames_save_path = "/data/yinzi/babyview_main_pose_val_set"
os.makedirs(tmp_frames_save_path, exist_ok=True)
all_videos_file_path = list(df["full_paths"])
for i, video_file_path in enumerate(all_videos_file_path):
    filename = df.iloc[i]["filename"]
    # basename = filename.replace(".MP4", "")
    if not os.path.exists(dataset_root_path+video_file_path):
        print(f"not exist: {dataset_root_path+video_file_path}")
    start_time = df.iloc[i]['start_time']
    end_time = df.iloc[i]['end_time']
    frames_save_path = os.path.join(tmp_frames_save_path, filename)
    os.makedirs(frames_save_path, exist_ok=True)
    # extract frames from video between start_time and end_time
    os.system(f"ffmpeg -i {dataset_root_path+video_file_path} -ss {start_time} -to {end_time} -r 1 -q:v 2 {frames_save_path}/%06d.jpg")

# %% for each video, random sample 1 frame from its 30 frames
# set random seed to reproduce results
import random
random.seed(2024)

val_set_save_path = "./babyview_main_pose_val_set"
os.makedirs(val_set_save_path, exist_ok=True)
for i, video_file_path in enumerate(all_videos_file_path):
    filename = df.iloc[i]["filename"]
    crrent_video_allframes_full_path = glob(f"{tmp_frames_save_path}/{filename}/*.jpg")
    chosen_frame = random.choice(crrent_video_allframes_full_path)
    # save 
    os.system(f"cp {chosen_frame} {val_set_save_path}/{filename}.jpg")
    




# %%
