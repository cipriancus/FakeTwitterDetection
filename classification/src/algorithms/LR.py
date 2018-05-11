import src.config as cfg
from sklearn.metrics import accuracy_score, confusion_matrix
from pyspark.ml.classification import NaiveBayes
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml import Pipeline
from pyspark.sql.functions import *


cfg.dir

features = ["Retweets", "Favorites", "New_Feature"]  # Class is label


class LogisticRegressionClassifier:

    def __init__(self, file_name, spark_context):
        self.sqlContext = SQLContext(spark_context)

        self.spark_context = spark_context

        self.data = self.sqlContext.read.options(header='true', inferschema='true', delimiter=',').csv(file_name)

        self.data.cache()

        lr_data = self.data.select(col("Class").alias("label"), *features)

        vectorAssembler = VectorAssembler(inputCols=features, outputCol="unscaled_features")

        standardScaler = StandardScaler(inputCol="unscaled_features", outputCol="features")

        self.nb = NaiveBayes(smoothing=1.0, modelType="multinomial")

        stages = [vectorAssembler, standardScaler, self.nb]

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

        x["Retweets"] = int(x["Retweets"])
        x["Favorites"] = float(x["Favorites"])

        data_frame = self.sqlContext.createDataFrame([x])
        output = self.model.transform(data_frame)
        return output.select(col("prediction")).collect()[0].prediction


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
        print("############################NB############################")
        print("Accuracy for NB " + str(accuracy))
        print("Confusion Matrix for NB")
        print(confusion_matrix(test_class, predict_list))
        print("##########################################################")
        return accuracy

    # def plot(self):
    #     import matplotlib.pyplot as plt
    #     from matplotlib.pyplot import *
    #     color = ['red' if label == 1 else 'green' for label in self.train_file['Class']]
    #     color_test = ['black' if label == 1 else 'blue' for label in self.test_data_predicted_label]
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')
    #     ax.scatter(self.train_file['Retweets'], self.train_file['Favorites'], self.train_file['New_Feature'],
    #                zdir='z', s=20, depthshade=True, color=color, marker='^')
    #     ax.scatter(self.test_file['Retweets'], self.test_file['Favorites'], self.test_file['New_Feature'],
    #                zdir='z', s=20, depthshade=True, color=color_test, marker='^')
    #     plt.title("NB Classifier")
    #     ax.set_xlabel('X axis')
    #     ax.set_ylabel('Y axis')
    #     ax.set_zlabel('Z axis')
    #     ax.legend(loc=2)
    #     plt.show()


if __name__ == "__main__":
    print("You are in main")
