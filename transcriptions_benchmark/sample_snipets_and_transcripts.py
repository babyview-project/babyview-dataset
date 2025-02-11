# %%
import os
import pandas as pd

# read in csv
df = pd.read_csv('to_sample_for_whisper.csv')
dataset_root_path = "/data/yinzi/babyview_20240507"
csv_root_path = "/data/yinzi/babyview_20240507/transcripts_distil-large-v3/Babyview_Main"
all_video_paths = list(df['full_paths'])

# %% sample transcripts
trascripts_target_path = "/data/yinzi/upload_to_drive/sampled_transcripts"
os.makedirs(trascripts_target_path, exist_ok=True)
all_file_names = list(df["filename"])
for file_name in all_file_names:
    # sub MP4 to csv
    csv_file_name = file_name.replace(".MP4", ".csv")
    subject_id = file_name.split("_")[0]
    csv_full_path = os.path.join(csv_root_path, subject_id, csv_file_name)
    if not os.path.exists(csv_full_path):
        print(f"File not found: {csv_full_path}")
        continue
    trascripts_target_full_path = os.path.join(trascripts_target_path, subject_id)
    os.makedirs(trascripts_target_full_path, exist_ok=True)
    # copty to trascripts_target_path
    cmd = f"cp {csv_full_path} {trascripts_target_full_path}"
    print(cmd)
    os.system(cmd)

# %% extract video snipets
video_snipets_target_path = "/data/yinzi/upload_to_drive/sampled_video_snipets"

os.makedirs(video_snipets_target_path, exist_ok=True)

for i, video_path in enumerate(all_video_paths):
    file_name = df.loc[i]['filename']
    base_name = file_name.replace(".MP4", "")
    video_full_path = dataset_root_path +  video_path
    if not os.path.exists(video_full_path):
        print(f"Video File not found: {video_full_path}")
        continue
    start_time = df.loc[i]['start_time']
    end_time = df.loc[i]['end_time']
    snipets_save_full_path = os.path.join(video_snipets_target_path, f"{base_name}_start_{start_time}_end_{end_time}_snipet.MP4")
    os.system(f"ffmpeg -i {video_full_path} -ss {start_time} -to {end_time} -c copy {snipets_save_full_path}")

# %%
