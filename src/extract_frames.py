import pytube
import sys
from tqdm.auto import tqdm
import pandas
import ffmpeg
import numpy as np
import torch
import cv2
import os

from os import walk

from decord import VideoReader
from decord import cpu, gpu

from extract_objects_yolo3 import detect_objects_single_image
from image_caption import get_caption_single_image

#frames = vr.get_batch([1, 3, 5, 7, 9])
#frames2 = vr.get_batch([1, 2, 3, 2, 3, 4, 3, 4, 5]).asnumpy()
#print(frames2.shape)
# (9, 240, 320, 3)

# 2. you can do cv2 style reading as well
# skip 100 frames
#vr.skip_frames(100)
# seek to start
#vr.seek(0)
#batch = vr.next()
#print('frame shape:', batch.shape)
#print('numpy frames:', batch.asnumpy())

#TODO: declare global csv file

def extract_frames_from_video(video_file, video_id, target_dir):
    """
    for each video file creates the corresponding directory if not exists 
    csv item: path_to_frame;frame_index;avg_fps;yolo3_classes;caption;
    """
    # a file like object works as well, for in-memory decoding
    with open(video_file, 'rb') as f:
        vr = VideoReader(f, ctx=cpu(0))
        print('video frames:', len(vr))
        total_frames = len(vr)
        avg_fps = vr.get_avg_fps()
        # 1. the simplest way is to directly access frames
        print('get_avg_fps=', vr.get_avg_fps())
        for i in range(len(vr)):
      #      # the video reader will handle seeking and skipping in the most efficient manner
            frame = vr[i]
            save_path = os.path.join(target_dir,"{:010d}.jpg".format(i))
            if not os.path.exists(save_path):
                print(frame.shape)
                img = frame.asnumpy()
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                detected_classes_list = detect_objects_single_image(img)
                words = get_caption_single_image(img)
                
          #      cv2.imwrite(save_path, img)
        #save frames into the dir

#clips can be used in the action recognition setup
#image
# we extarcted frames, then we computed differences between frames using the following method
# if there no difference in the consecutive frames, the frame is removed from the classification
# it is done in order to neglagate the bias

def get_frames_and_save(video_dir):
    video_files = []
    for (dirpath, dirnames, filenames) in walk(video_dir):
        for f in filenames:
            if f.endswith('.mp4'):
                video_id = f.split('.mp4')[0]
                print(video_id)
                target_dir = os.path.join(video_dir, video_id)
                video_file = os.path.join(video_dir, f)
                print(target_dir)
                os.makedirs(target_dir, exist_ok=True)
                extract_frames_from_video(video_file, video_id, target_dir)
                return
  

if __name__ == '__main__': 

    video_folder = sys.argv[1] 
    get_frames_and_save(video_folder)