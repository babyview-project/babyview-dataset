# %%
import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Load the COCO format data
with open('babyview_pose_val_coco_format.json') as f:
    data = json.load(f)

# Initialize dictionaries to hold counts
people_count = {}
keypoints_count = {}
elements_count = {'face': {}, 'body': {}, 'left_hand': {}, 'right_hand': {}}

# Define keypoints indices
face_indices = [0, 1, 2, 3, 4]
body_indices = [5, 6, 11, 12, 13, 14, 15, 16]
left_hand_indices = [7, 9]
right_hand_indices = [8, 10]

# Process each annotation
for annotation in data['annotations']:
    image_id = annotation['image_id']
    
    # Initialize count if not already done
    if image_id not in people_count:
        people_count[image_id] = 0
        keypoints_count[image_id] = 0
        elements_count['face'][image_id] = 0
        elements_count['body'][image_id] = 0
        elements_count['left_hand'][image_id] = 0
        elements_count['right_hand'][image_id] = 0
    
    # Count valid bounding boxes
    if annotation['area'] > 0:
        people_count[image_id] += 1
    
    # Count keypoints
    num_valid_keypoints = sum(1 for k in annotation['keypoints'] if k != [0, 0])
    keypoints_count[image_id] += num_valid_keypoints
    
    # Check for face, body, left hand, right hand keypoints
    has_face = any(annotation['keypoints'][i] != [0, 0] for i in face_indices)
    has_body = any(annotation['keypoints'][i] != [0, 0] for i in body_indices)
    has_left_hand = any(annotation['keypoints'][i] != [0, 0] for i in left_hand_indices)
    has_right_hand = any(annotation['keypoints'][i] != [0, 0] for i in right_hand_indices)
    
    if has_face:
        elements_count['face'][image_id] += 1
    if has_body:
        elements_count['body'][image_id] += 1
    if has_left_hand:
        elements_count['left_hand'][image_id] += 1
    if has_right_hand:
        elements_count['right_hand'][image_id] += 1

# Convert dictionaries to DataFrames for visualization
people_df = pd.DataFrame(list(people_count.items()), columns=['Image ID', 'People Count'])
elements_df = pd.DataFrame({
    'Image ID': list(elements_count['face'].keys()),
    'Face Count': list(elements_count['face'].values()),
    'Body Count': list(elements_count['body'].values()),
    'Left Hand Count': list(elements_count['left_hand'].values()),
    'Right Hand Count': list(elements_count['right_hand'].values())
})

# Set 'Image ID' as the index
elements_df.set_index('Image ID', inplace=True)
people_df.set_index('Image ID', inplace=True)

# Apply seaborn style
sns.set(style="whitegrid")

# Plot the people count bar chart with swapped axes
plt.figure(figsize=(10, 12))
sns.barplot(y=people_df.index, x=people_df['People Count'], palette="Blues_d", orient='h')
plt.ylabel('Image ID', fontsize=14)
plt.xlabel('People Count', fontsize=14)
plt.title('Number of People per Image', fontsize=16)
plt.tight_layout()
plt.show()

# Plot the stacked bar chart for keypoints with swapped axes
elements_df.plot(kind='barh', stacked=True, figsize=(12, 10), color=sns.color_palette("muted"))
plt.ylabel('Image ID', fontsize=14)
plt.xlabel('Count', fontsize=14)
plt.title('Count of Face, Body, Left Hand, and Right Hand Keypoints per Image', fontsize=16)
plt.legend(title='Keypoint Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Count the number of images with different numbers of people
people_distribution = people_df['People Count'].value_counts().sort_index()

# Plot the distribution of the number of people per image
plt.figure(figsize=(10, 6))
sns.barplot(x=people_distribution.index, y=people_distribution.values, palette="viridis")
plt.xlabel('Number of People', fontsize=14)
plt.ylabel('Number of Images', fontsize=14)
plt.title('Distribution of Number of People per Image', fontsize=16)
plt.tight_layout()
plt.show()
