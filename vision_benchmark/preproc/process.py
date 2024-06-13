import os
import cv2
import numpy as np
import logging
import glob 
import argparse

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1" 
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1" 
os.environ["NUMEXPR_NUM_THREADS"] = "1" 

from multiprocessing import Process
from datetime import datetime
from tqdm import tqdm

def resize_frame(frame, shortest_side=720):
    """
    Resizes a frame maintaining aspect ratio so that the shortest side length is `shortest_side` pixels.

    Args:
        frame (numpy.ndarray): Input frame as a NumPy array.
        shortest_side (int): Desired length of the shortest side after resizing.

    Returns:
        numpy.ndarray: Resized frame.
    """
    # Calculate the aspect ratio
    height, width, _ = frame.shape
    aspect_ratio = width / height

    # Resize the frame
    if height <= width:
        new_height = shortest_side
        new_width = int(aspect_ratio * new_height)
    else:
        new_width = shortest_side
        new_height = int(new_width / aspect_ratio)

    return cv2.resize(frame, (new_width, new_height), cv2.INTER_AREA)


def process_video(video_path, output_dir, target_framerate=5):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fps = int(np.round(fps))
    # Calculate frame interval for subsampling
    interval = fps // target_framerate
    
    # Process frames
    count = 0
    while True:
        #print(count, total_frames, end='\r')
        ret, frame = cap.read()
        if not ret:
            break
        
        # Only process frames at the specified interval
        if count % interval == 0:
            # Resize frame
            frame_resized = resize_frame(frame)
            
            # Save resized frame as JPEG
            frame_name = os.path.join(output_dir, f"{count:06d}.jpg")
            cv2.imwrite(frame_name, frame_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
            
        count += 1
    
    # Release video capture object
    cap.release()

def setup_logger(log_root):
    """
    Set up a logger to log errors with the current date and time.
    """
    log_file = os.path.join(log_root, f"proc_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    logging.basicConfig(filename=log_file, level=logging.ERROR, format='%(asctime)s %(message)s')


def worker(videos, output_root, log_root, shortest_side):
    
    setup_logger(log_root)
    for video in tqdm(videos, desc="Processing videos"):

        vid_name = os.path.split(video)[-1]
        vid_name = vid_name[:-4]

        output_dir = os.path.join(output_root, vid_name)
        try: 
            process_video(video, output_dir, shortest_side=360)
            logging.info(f"success: {vid_name}")
        except Exception as e:
            print(e)
            logging.error(f"error: {vid_name} {e}")


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--video_root', type=str, required=True, help='Path to the root directory of videos')
    parser.add_argument('--output_root', type=str, required=True, help='Path to the output directory')
    parser.add_argument('--shortest_side', type=int, default=360, help='Shortest side (in pixels) of extracted frames')

    args = parser.parse_args()
    
    video_root = args.video_root
    output_root = args.output_root
    shortest_side = args.shortest_side
    
    print(f'Video Root: {video_root}')
    print(f'Output Root: {output_root}')

    log_root = "proc_logs"

    os.makedirs(log_root, exist_ok=True)

    videos = glob.glob(f"{args.video_root}/*/*")

    num_processes = 16
    videos_per_process = len(videos) // num_processes + (len(videos) % num_processes > 0)

    processes = []
    for i in range(num_processes):
        start_index = i * videos_per_process
        end_index = start_index + videos_per_process
        videos_proc = videos[start_index:end_index]

        p = Process(target=worker, args=(videos_proc, output_root, log_root, shortest_side))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
 

if __name__ == "__main__":
    main()

