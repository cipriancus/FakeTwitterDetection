import src.config as cfg
from sklearn.metrics import accuracy_score, confusion_matrix
from pyspark.ml.classification import LinearSVC
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml import Pipeline
from pyspark.sql.functions import *

cfg.dir
# warnings.filterwarnings("ignore")
features = ["Retweets", "Favorites", "New_Feature"]  # Class is label


class SVMClassifier(object):

    def __init__(self, file_name, spark_context):
        self.sqlContext = SQLContext(spark_context)

        self.data = self.sqlContext.read.options(header='true', inferschema='true', delimiter=',').csv(file_name)

        self.data.cache()

        lr_data = self.data.select(col("Class").alias("label"), *features)

        vectorAssembler = VectorAssembler(inputCols=features, outputCol="unscaled_features")

        standardScaler = StandardScaler(inputCol="unscaled_features", outputCol="features")

        self.SVM = LinearSVC(maxIter=10, regParam=.01)

        stages = [vectorAssembler, standardScaler, self.SVM]

        pipeline = Pipeline(stages=stages)

        self.model = pipeline.fit(lr_data)

    def classify_testdata(self, filename):
        """
          Function that classifies the testing dataset
          :param filename: The filename that contains the testing dataset
          :return: The predicted labels for the testing dataset
        """
        self.test_file = self.sqlContext.read.format('csv').options(header='true', inferschema='true').load(filename)

        lr_data = self.test_file.select(col("Class").alias("label"), *features)

        prediction = self.model.transform(lr_data)

        return prediction

    def classify(self, x):
        """
        Function that classifies an entry
        :param x: Entry to be predicted
        :return: The predicted label
        """
        output = self.model.fit(x)
        return output

    def confusion_matrix(self, predict):
        """
        Function that computes confusion matrix to evaluate the accuracy of the classification
        :param predict: The predicted labels that is used to compute the confusion matrix
        :return: The confusion matrix
        """
        predict_list = [i.prediction for i in predict.select("prediction").collect()]
        test_class = [i.Class for i in self.test_file.select("Class").collect()]  # self.test_file['Class']
        accuracy = accuracy_score(test_class, predict_list)
        accuracy = accuracy * 100
        print("###########################SVM############################")
        print("Accuracy for SVM " + str(accuracy))
        print("Confusion Matrix for SVM")
        print(confusion_matrix(test_class, predict_list))
        print("##########################################################")
        return accuracy

    # def plot(self):
    #     import matplotlib.pyplot as plt
    #     from matplotlib.pyplot import *
    #     from mpl_toolkits.mplot3d import Axes3D
    #
    #     """
    #     Function that builds the 3D plot
    #     :return:
    #     """
    #     color = ['red' if l == 1 else 'black' for l in self.train_file['Class']]
    #     color_test = ['green' if l == 1 else 'blue' for l in self.test_data_predicted_label]
    #     z = lambda x, y: (-self.SVM.intercept_[0] - self.SVM.coef_[0][0] * x - self.SVM.coef_[0][1]) / \
    #                      self.SVM.coef_[0][2]
    #     tmp = np.linspace(1, 140, 14)
    #     x, y = np.meshgrid(tmp, tmp)
    #     fig = plt.figure()
    #     ax = Axes3D(fig)
    #     ax.plot_surface(x, y, z(x, y))
    #     ax.scatter(self.train_file['Retweets'], self.train_file['Favorites'],
    #                self.train_file['New_Feature'], zdir='z', s=20, depthshade=True, color=color, marker='*')
    #     ax.scatter(self.test_file['Retweets'], self.test_file['Favorites'], self.test_file['New_Feature'], zdir='z',
    #                s=20, depthshade=True, color=color_test, marker='*')
    #     plt.title("SVM Classifier")
    #     ax.set_xlabel('X axis')
    #     ax.set_ylabel('Y axis')
    #     ax.set_zlabel('Z axis')
    #     ax.legend(loc=2)
    #     plt.show()


if __name__ == "__main__":
    print("You are in main")
