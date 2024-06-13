import os
from PIL import Image
import glob
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help='Path to the extracted images')

    args = parser.parse_args()
 
    path = args.path
    items = glob.glob(f"{path}/*/*")

    items = [x.replace(path+'/', '') for x in items]

    to_output = [x+'\n' for x in items]

    with open('data_list.txt', "w") as f:
        f.writelines(to_output)

if __name__ == "__main__":
    main()
