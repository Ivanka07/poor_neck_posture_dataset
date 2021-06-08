print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from feature_extractor import FeatureExtractor 
from posture_classifier import PoseClassifier
import sys
import os



CLASS_NAMES = ['text_neck', 'poor_sitting_posture', 'correct_standing_posture', 'correct_sitting_posture']


def classify_single_frame(path_to_poses):
    files = os.listdir(path_to_poses)
    #feature vectors
    X_data =  []
    #class_ids
    y_data = []
    
    for file in files:
        print(file)
        if not file.endswith('.json'):
            continue
        file = path_to_poses + file
        features, cl_id = extract_features(file)
    

        for f_vector in features:
            feature_list = []
            for item in f_vector:
                
                if  isinstance(item, np.ndarray):
                    feature_list.append(item[0])
                    feature_list.append(item[1])
                else:
                    feature_list.append(item)


            X_data.append(feature_list)
            y_data.append(cl_id)

    classifier = PoseClassifier(X_data, y_data, CLASS_NAMES)
    classifier.classifySVN()

def classify_features(path_to_poses):
    files = os.listdir(path_to_poses)
    #feature vectors
    X_data =  []
    #class_ids
    y_data = []
    
    for file in files:
        print(file)
        if not file.endswith('.json'):
            continue
        file = path_to_poses + file
        features, cl_id = extract_features(file)
    

        for f_vector in features:
            feature_list = []
            for item in f_vector:
                
                if  isinstance(item, np.ndarray):
                    feature_list.append(item[0])
                    feature_list.append(item[1])
                else:
                    feature_list.append(item)

            X_data.append(feature_list)
            y_data.append(cl_id)

    classifier = PoseClassifier(X_data, y_data, CLASS_NAMES)
    classifier.classifySVN()


def extract_features(json_file):
    class_id = json_file.split('_')[-1]
    class_id = int(class_id[0])
    feature_extractor = FeatureExtractor(json_file)
    feature_list = feature_extractor.extract_features()

    return feature_list, class_id





if __name__ == '__main__':

    path_to_data = sys.argv[1] 
    classify_single_frame(path_to_data)


