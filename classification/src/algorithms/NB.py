import src.config as cfg
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import *
from sklearn import metrics
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.naive_bayes import GaussianNB

warnings.filterwarnings('ignore')

cfg.dir

pd.set_option('display.max_colwidth', 30000)

columns_header = ['Retweets', 'Favorites', 'New_Feature', 'Class']

cols = ['Class']
mycol = ['Retweets', 'Favorites', 'New_Feature']


class NbClassifier:

    def __init__(self, file_name):
        self.train_file = pd.read_csv(file_name, sep=",", usecols=columns_header, index_col=None)

        train_data = np.array(self.train_file.values[:, :3])
        train_data_labels = self.train_file['Class']

        # init the model
        self.NB = GaussianNB()
        self.NB.fit(train_data, train_data_labels)

        self.accuracy = 0

    def classify_testdata(self, testing_file):
        self.test_file = pd.read_csv(testing_file, sep=',', usecols=columns_header, index_col=None)
        self.test_data = np.array(self.test_file.values[:, :3])
        self.test_data_predicted_label = self.NB.predict(self.test_data)
        return self.test_data_predicted_label

    def classify(self, x):
        output = self.NB.predict(x)
        probability = self.NB.predict_proba(x)
        return output, probability

    def plot(self):
        color = ['red' if label == 1 else 'green' for label in self.train_file['Class']]
        color_test = ['black' if label == 1 else 'blue' for label in self.test_data_predicted_label]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.train_file['Retweets'], self.train_file['Favorites'], self.train_file['New_Feature'],
                   zdir='z', s=20, depthshade=True, color=color, marker='^')
        ax.scatter(self.test_file['Retweets'], self.test_file['Favorites'], self.test_file['New_Feature'],
                   zdir='z', s=20, depthshade=True, color=color_test, marker='^')
        plt.title("NB Classifier")
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.legend(loc=2)
        plt.show()

    def confusion_matrix(self, predict):
        accuracy = accuracy_score(self.test_file['Class'], predict)
        accuracy = accuracy * 100
        print("############################NB############################")
        print("Accuracy for NB " + str(accuracy))
        print()
        print("Confusion Matrix for KNN")
        print(confusion_matrix(self.test_file['Class'], predict))
        print("##########################################################")
        return accuracy


if __name__ == "__main__":
    print("You are in main")
