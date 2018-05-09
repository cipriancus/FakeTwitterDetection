import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import *
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
import src.config as cfg

cfg.dir
warnings.filterwarnings("ignore")
pd.set_option('display.max_colwidth', 30000)
columns_header = ['Retweets', 'Favorites', 'New_Feature', 'Class']


class KNNClassifier(object):

    def __init__(self, file_name, n_neighbors_param=101):
        # Load training csv
        self.train_file = pd.read_csv(file_name, sep=',', usecols=columns_header, index_col=None)

        train_data = np.array(self.train_file.values[:, :3])
        train_data_labels = self.train_file['Class']
        # init the model
        self.KNN = KNeighborsClassifier(n_neighbors=n_neighbors_param)
        self.KNN.fit(train_data, train_data_labels.values)

    def classify_testdata(self, filename):
        """
        Function that classifies the testing dataset
        :param filename: The filename that contains the testing dataset
        :return: The predicted labels for the testing dataset
        """

        self.test_file = pd.read_csv(filename, sep=',', usecols=columns_header, index_col=None)
        self.test_data = np.array(self.test_file.values[:, :3])
        self.test_data_predicted_label = self.KNN.predict(self.test_data)
        return self.test_data_predicted_label

    def classify(self, x):
        """
        Function that classifies an entry
        :param x: Entry to be predicted
        :return: The predicted label
        """
        output = self.KNN.predict(x)
        return output

    def confusion_matrix(self, predict):
        """
        Function that computes confusion matrix to evaluate the accuracy of the classification
        :param predict: The predicted labels that is used to compute the confusion matrix
        :return: The confusion matrix
        """
        accuracy = accuracy_score(self.test_file['Class'], predict)
        accuracy = accuracy * 100
        print("###########################KNN############################")
        print("Accuracy for KNN " + str(accuracy))
        print("Confusion Matrix for KNN")
        print(confusion_matrix(self.test_file['Class'], predict))
        print("##########################################################")
        return accuracy

    def plot(self):
        """
        Function that builds the 3D plot
        :return:
        """
        color = ['red' if label == 1 else 'green' for label in self.train_file['Class']]
        color_test = ['black' if label == 1 else 'blue' for label in self.test_data_predicted_label]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(self.train_file['Retweets'], self.train_file['Favorites'], self.train_file['New_Feature'],
                   zdir='z', s=20, depthshade=True, color=color, marker='^')
        ax.scatter(self.test_file['Retweets'], self.test_file['Favorites'], self.test_file['New_Feature'],
                   zdir='z', s=20, depthshade=True, color=color_test, marker='^')
        plt.title("KNN Classifier")
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.legend(loc=2)
        plt.show()


if __name__ == "__main__":
    print("You are in main")
