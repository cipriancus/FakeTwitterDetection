import src.config as cfg
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
from sklearn import svm
from sklearn.metrics import accuracy_score, confusion_matrix

cfg.dir
warnings.filterwarnings("ignore")
pd.set_option('display.max_colwidth', 30000)
My_col = ['Retweets', 'Favorites', 'New_Feature', 'Class']


class SVMClassifier(object):

    def __init__(self, file_name):
        # Load training csv
        self.train_file = pd.read_csv(file_name, sep=',', usecols=My_col, index_col=None)

        train_data = np.array(self.train_file.values[:, :3])
        train_data_labels = self.train_file['Class']
        # init the model
        self.SVM = svm.SVC(kernel='linear', C=1.0, gamma=2)
        self.SVM.fit(train_data, train_data_labels.values)

        self.accuracy = 0
        self.output = []

    def classify_testdata(self, filename):
        """
          Function that classifies the testing dataset
          :param filename: The filename that contains the testing dataset
          :return: The predicted labels for the testing dataset
        """

        self.test_file = pd.read_csv(filename, sep=',', usecols=My_col, index_col=None)
        self.test_data = np.array(
            [self.test_file['Retweets'], self.test_file['Favorites'], self.test_file['New_Feature']])
        self.test_data = np.array(self.test_file.values[:, :3])
        self.test_data_predicted_label = self.SVM.predict(self.test_data)
        return self.test_data_predicted_label

    def classify(self, x):
        """
        Function that classifies an entry
        :param x: Entry to be predicted
        :return: The predicted label
        """
        output = self.SVM.predict(x)
        return output

    def confusion_matrix(self, predict):
        """
        Function that computes confusion matrix to evaluate the accuracy of the classification
        :param predict: The predicted labels that is used to compute the confusion matrix
        :return: The confusion matrix
        """
        accuracy = accuracy_score(self.test_file['Class'], predict)
        accuracy = accuracy * 100
        print("###########################SVM############################")
        print("Accuracy for SVM " + str(accuracy))
        print("Confusion Matrix for SVM")
        print(confusion_matrix(self.test_file['Class'], predict))
        print("##########################################################")
        return accuracy

    def plot(self):
        """
        Function that builds the 3D plot
        :return:
        """
        color = ['red' if l == 1 else 'black' for l in self.train_file['Class']]
        color_test = ['green' if l == 1 else 'blue' for l in self.test_data_predicted_label]
        z = lambda x, y: (-self.SVM.intercept_[0] - self.SVM.coef_[0][0] * x - self.SVM.coef_[0][1]) / \
                         self.SVM.coef_[0][2]
        tmp = np.linspace(1, 140, 14)
        x, y = np.meshgrid(tmp, tmp)
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.plot_surface(x, y, z(x, y))
        ax.scatter(self.train_file['Retweets'], self.train_file['Favorites'],
                   self.train_file['New_Feature'], zdir='z', s=20, depthshade=True, color=color, marker='*')
        ax.scatter(self.test_file['Retweets'], self.test_file['Favorites'], self.test_file['New_Feature'], zdir='z',
                   s=20, depthshade=True, color=color_test, marker='*')
        plt.title("SVM Classifier")
        ax.set_xlabel('X axis')
        ax.set_ylabel('Y axis')
        ax.set_zlabel('Z axis')
        ax.legend(loc=2)
        plt.show()


if __name__ == "__main__":
    print("You are in main")
