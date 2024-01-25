import os
import cv2

def get_resolution(video_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(3))
    height = int(cap.get(4))
    cap.release()
    return width, height

def rename_wrong_resolution_videos(folder_path):
    print("xx")
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):
            video_path = os.path.join(folder_path, filename)
            width, height = get_resolution(video_path)
            
            if width != 1920 or height != 1080:
                new_filename = f"wrong {filename}"
                new_path = os.path.join(folder_path, new_filename)
                os.rename(video_path, new_path)
                print(f'Renamed: {filename} -> {new_filename}')

if __name__ == "__main__":
    folder_path = "/Users/ric/code/tiktokvideogen/Clips"
    print("xx")
    rename_wrong_resolution_videos(folder_path)
