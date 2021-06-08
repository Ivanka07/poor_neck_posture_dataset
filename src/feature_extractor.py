import json
import numpy as np
import sys
import os


class Pose():
    """Pose is represented by a dictionary
        where the keys are the landmark ids;
        the corresponding values are x,y,z coordinates and the confidence
        torso multiplier is taken from: 
            https://colab.research.google.com/drive/19txHpN8exWhstO6WVkfmYYVC6uug_oVR#scrollTo=QBrKOeP30RAx
    """


    def __init__(self, values):
        
        self.landmark_names = [
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
        'left_foot_index', 'right_foot_index'
        ]

        self.torso_multiplier = 2.5 
        self.landmarks = {}

        self.asign_values(values)

    def asign_values(self, values):

        assert len(values) == len(self.landmark_names)
        for i, landmark in enumerate(self.landmark_names):
            self.landmarks[landmark] = values[i]
    
    def print_pose(self):
        for key, value in self.landmarks.items():
            print(key, ' =', value)

    def normilize(self):
        normilized_landmarks = {}
        left_hip = np.copy(self.landmarks['left_hip'][0:3])
        right_hip = np.copy(self.landmarks['right_hip'][0:3])
        #hip is defined by the model as a pose center
        hip_center = (left_hip + right_hip)*0.5

        left_shoulder = np.copy(self.landmarks['left_shoulder'][0:3])
        right_shoulder = np.copy(self.landmarks['right_shoulder'][0:3])
        shoulder_center = (left_hip + right_hip)*0.5

        #torso size in 2D
        torso_size = np.linalg.norm(shoulder_center[0:2] - hip_center[0:2])
        #calculate dist to each landmark
        distances = []
        
        for land_coord in self.landmarks.values():
            distances.append(np.linalg.norm(land_coord[0:3] - hip_center))

        max_dist = max(distances)
        pose_size = max(torso_size * self.torso_multiplier, max_dist)
        
        for key, value in self.landmarks.items():
            normilized_landmarks[key] = np.copy(value[0:3]) / pose_size
        return normilized_landmarks

class FeatureExtractor():
    """FeatureDetector
    The following distances are extracted: 
    - nose - l wrist
    - nose - r wrist
    - nose - l shoulder
    - nose - r shoulder
    - l shoulder - l wrist
    - r shoulder - r wrist
    - l hip - l wrist
    - r hip - r wrist
    - l hip - l ankle
    - r hip - r ankle
    
    The following angles are extracted:
    - l hip - l wrist
    - r hip - r wrist
    - l hip - l ankle
    - r hip - r ankle


    """
    def __init__(self, json_file):

        self.json_file = json_file
        self.joint_distance = [] 
        self.joint_angles = []


    def extract_features(self):
        features = []
        with open(self.json_file) as f:
            data = json.load(f)
           # print(len(data['data']))
            for key, value in data['data'].items():
               #print(key)
                keypoints = data['data'][key]['person00'] 
               # print(len(keypoints))
                if len(keypoints) == 33:
                    pose = Pose(keypoints)
                    coordinates = np.array(self.extract_2d_coordinates(pose))
                    _features = self.extract_single_frame(pose)
                    concat = np.concatenate((_features, coordinates), axis=0)
                   # features.append(self.extract_single_frame(pose))
                    features.append(concat)
        return features

    def extract_2d_coordinates(self, pose):
        """Extract defined features from a single frame
        :param Pose pose
        :return array features
        """
        normilized_lmks = pose.normilize()

        values = []
        for v in normilized_lmks.values():
            values.append(v[0])
            values.append(v[1])
        return values


    def extract_single_frame(self, pose):
        """Extract defined features from a single frame
        :param Pose pose
        :return array features
        """
        normilized_lmks = pose.normilize()
        features = np.array([
    #        self.get_distance_by_names(normilized_lmks, 'nose', 'left_ankle'),
    #        self.get_distance_by_names(normilized_lmks, 'nose', 'right_ankle'),
    #       self.get_distance_by_names(normilized_lmks, 'nose', 'left_shoulder'),
    #        self.get_distance_by_names(normilized_lmks, 'nose', 'right_shoulder'),

            self.get_distance_by_names(normilized_lmks, 'nose', 'left_wrist'),
            self.get_distance_by_names(normilized_lmks, 'nose', 'right_wrist'),
            self.get_distance_by_names(normilized_lmks, 'left_shoulder', 'left_wrist'),
            self.get_distance_by_names(normilized_lmks, 'right_shoulder', 'right_wrist'),
            self.get_distance_by_names(normilized_lmks, 'left_shoulder', 'right_wrist'),
            self.get_distance_by_names(normilized_lmks, 'right_shoulder', 'left_wrist'),
            self.get_distance_by_names(normilized_lmks, 'left_hip', 'left_wrist'),
            self.get_distance_by_names(normilized_lmks, 'right_hip', 'right_wrist'),
            self.get_distance_by_names(normilized_lmks, 'left_hip', 'right_wrist'),
            self.get_distance_by_names(normilized_lmks, 'right_hip', 'left_wrist'),
            self.get_distance_by_names(normilized_lmks, 'left_hip', 'left_shoulder'),
            self.get_distance_by_names(normilized_lmks, 'right_hip', 'right_shoulder'),
            self.get_distance_by_names(normilized_lmks, 'left_hip', 'right_shoulder'),
            self.get_distance_by_names(normilized_lmks, 'right_hip', 'left_shoulder'),
            self.get_distance_by_names(normilized_lmks, 'left_elbow', 'left_wrist'),
            self.get_distance_by_names(normilized_lmks, 'right_elbow', 'right_wrist'),
            self.get_distance_by_names(normilized_lmks, 'left_elbow', 'right_wrist'),
            self.get_distance_by_names(normilized_lmks, 'right_elbow', 'left_wrist'),
            self.get_distance_by_names(normilized_lmks, 'left_hip', 'left_ankle'),
            self.get_distance_by_names(normilized_lmks, 'right_hip', 'right_ankle'),
            self.get_distance_by_names(normilized_lmks, 'left_hip', 'right_ankle'),
            self.get_distance_by_names(normilized_lmks, 'right_hip', 'left_ankle'),
            self.get_distance_by_names(normilized_lmks, 'right_ankle', 'right_shoulder'),
            self.get_distance_by_names(normilized_lmks, 'left_ankle', 'left_shoulder'),
            self.get_angle_by_names(normilized_lmks, 'right_shoulder', 'right_elbow', 'right_wrist'),
            self.get_angle_by_names(normilized_lmks, 'left_shoulder', 'left_elbow', 'left_wrist'),
            self.get_angle_by_names(normilized_lmks, 'right_shoulder', 'right_hip', 'right_knee'),
            self.get_angle_by_names(normilized_lmks, 'left_shoulder', 'left_hip', 'left_knee'),
            self.get_angle_by_names(normilized_lmks, 'right_shoulder', 'right_hip', 'right_ankle'),
            self.get_angle_by_names(normilized_lmks, 'left_shoulder', 'left_hip', 'left_ankle'),
            self.get_angle_by_names(normilized_lmks, 'right_hip', 'right_knee', 'right_ankle'),
            self.get_angle_by_names(normilized_lmks, 'left_hip', 'left_knee', 'left_ankle'),
            ]
            )
        return features

        
    def get_average_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[name_from]
        lmk_to = landmarks[name_to]
        return (lmk_from + lmk_to) * 0.5

    def get_distance_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[name_from][0:2]
        lmk_to = landmarks[name_to][0:2]
       # dist = np.linalg.norm(lmk_to - lmk_from)
        dist = lmk_to - lmk_from
        return dist

    def get_angle_by_names(self, landmarks, name_1, name_2, name_3):
        p0 = landmarks[name_1][0:2]
        p1 = landmarks[name_2][0:2]
        p2 = landmarks[name_3][0:2]

        v0 = np.array(p0) - np.array(p1)
        v1 = np.array(p2) - np.array(p1)

        angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
      #  print(np.degrees(angle))

        return angle


