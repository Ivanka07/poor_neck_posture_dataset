import json
import numpy as np
import sys
import os


class Pose():
    """Pose is represented by a dictionary
        where the keys are the landmark ids;
        the corresponding values are x,y,z coordinates and the confidence
    """
    landmark_names = [
        'nose',
        'left_eye_inner', 'left_eye', 'left_eye_outer',
        'right_eye_inner', 'right_eye', 'right_eye_outer',
        'left_ear', 'right_ear',
        'mouth_left', 'mouth_right',
        'left_shoulder', 'right_shoulder',
        'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist',
        'left_pinky_1', 'right_pinky_1',
        'left_index_1', 'right_index_1',
        'left_thumb_2', 'right_thumb_2',
        'left_hip', 'right_hip',
        'left_knee', 'right_knee',
        'left_ankle', 'right_ankle',
        'left_heel', 'right_heel',
        'left_foot_index', 'right_foot_index',
    ]


    def __init__(self, values):
        self.pose = self.asign_values(values)

    def asign_values(self, values):

        assert len(values) == len(landmark_names)
        for i, landmark in enumerate(landmark_names):
            self.pose[landmark] = values[i]


class FeatureExtractor():
    """FeatureDetector"""

    def __init__(self, json_file):

        self.json_file = json_file
        self.joint_distance = [] 
        self.joint_angles = [] 


    def extract_features(self):
        with open(self.json_file) as f:
            data = json.load(f)
            print(len(data['data']))
            init_pose = data['data']['frame0002']['person00']



    def extract_single_frame(self, frame):
        """Extract defined features from a single frame.
        :param numpy.ndarray frame
        """
        return NotImplemented


    def normilize_single_pose(self, pose):
        pass


if __name__ == '__main__':
    json_file = '../data/JMU2zYrLnK8_10_12.mp4.json'
    feature_extractor = FeatureExtractor(json_file)
    feature_extractor.extract_features()
