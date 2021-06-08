import json
import numpy as np
import sys
import os
import matplotlib.pyplot as plt  
from sklearn.datasets import make_classification
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC



#outlier detection 
#classification

class PoseClassifier():

    def __init__(self, features, targets, class_names):
        self.X_train, self.X_test, self.y_train, self.y_test = \
                            train_test_split(features, targets, random_state=0)
        self.class_names = class_names

    def classifySVN(self):
        print('SVN classifier initialization')
        classifier = SVC(kernel='linear', C=0.001, gamma='scale', verbose=True).fit(self.X_train, self.y_train)
        np.set_printoptions(precision=2)
        titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
        print('confusion_matrix building')
        print(classifier.score(self.X_test, self.y_test))
        for title, normalize in titles_options:
            disp = plot_confusion_matrix(classifier, self.X_test, self.y_test,
                                 display_labels=self.class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
            disp.ax_.set_title(title)

            print(title)
            print(disp.confusion_matrix)

            plt.show()
    def classifyKnn(self):
        print('SVN classifier initialization')
        classifier = KNeighborsClassifier(n_neighbors=3, verbose=True).fit(self.X_train, self.y_train)
        np.set_printoptions(precision=2)
        titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
        print('confusion_matrix building')
        print(classifier.score(self.X_test, self.y_test))
        for title, normalize in titles_options:
            disp = plot_confusion_matrix(classifier, self.X_test, self.y_test,
                                 display_labels=self.class_names,
                                 cmap=plt.cm.Blues,
                                 normalize=normalize)
            disp.ax_.set_title(title)

            print(title)
            print(disp.confusion_matrix)
        
    
    def plot_conf_mat(self):
        pass
