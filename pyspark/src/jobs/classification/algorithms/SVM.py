from sklearn.metrics import accuracy_score, confusion_matrix
from pyspark.ml.classification import LinearSVC
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml import Pipeline
from pyspark.sql.functions import *

features = ["Retweets", "Favorites", "New_Feature"]  # Class is label

class SVMClassifier(object):

    def __init__(self, file_name, spark_context, maxIter=100, regParam=0.0, tol=1e-6, threshold=0.0,
                 aggregationDepth=2):
        self.sqlContext = SQLContext(spark_context)

        self.spark_context = spark_context

        self.data = self.sqlContext.read.options(header='true', inferschema='true', delimiter=',').csv(file_name)

        self.data.cache()

        self.lr_data = self.data.select(col("Class").alias("label"), *features)

        vectorAssembler = VectorAssembler(inputCols=features, outputCol="unscaled_features")

        standardScaler = StandardScaler(inputCol="unscaled_features", outputCol="features")

        self.settings = [('maxIter',maxIter), ('regParam',regParam), ('tol',tol), ('threshold',threshold),('aggregationDepth',aggregationDepth)]

        self.SVM = LinearSVC(maxIter=maxIter, regParam=regParam, tol=tol, threshold=threshold,
                             aggregationDepth=aggregationDepth)

        stages = [vectorAssembler, standardScaler, self.SVM]

        pipeline = Pipeline(stages=stages)

        self.model = pipeline.fit(self.lr_data)

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
        print("###########################SVM############################")
        print("Accuracy for SVM " + str(accuracy))
        print("Confusion Matrix for SVM with settings" + str(self.settings))
        print(confusion_matrix(test_class, predict_list))
        print("##########################################################")
        return accuracy

    # def plot(self, predict):
    #     """
    #     Function that builds the 3D plot
    #     :return:
    #     """
    #     columns_header = ['Retweets', 'Favorites', 'New_Feature', 'Class']
    #
    #     testing_file_location = 'Test_feature_extracted.csv'
    #     training_file_location = 'Training_feature_extracted.csv'
    #
    #     train_file = pd.read_csv(training_file_location, sep=",", usecols=columns_header, index_col=None)
    #     test_file = pd.read_csv(testing_file_location, sep=',', usecols=columns_header, index_col=None)
    #
    #     train = [i.label for i in self.lr_data.select("label").collect()]
    #     test_class = [i.prediction for i in predict.select("prediction").collect()]
    #
    #     color = ['red' if label == 1 else 'green' for label in train]
    #     color_test = ['black' if label == 1 else 'blue' for label in test_class]
    #
    #     coef_values = self.model.stages[2].coefficients.values.tolist()
    #
    #     z = lambda x, y: (-self.model.stages[2].intercept - coef_values[0] * x - coef_values[1]) / coef_values[2]
    #     tmp = np.linspace(1, 140, 14)
    #     x, y = np.meshgrid(tmp, tmp)
    #     fig = plt.figure()
    #     ax = Axes3D(fig)
    #     ax.plot_surface(x, y, z(x, y))
    #     ax.scatter(train_file['Retweets'], train_file['Favorites'],train_file['New_Feature'], zdir='z', s=20, depthshade=True, color=color, marker='*')
    #     ax.scatter(test_file['Retweets'], test_file['Favorites'], test_file['New_Feature'], zdir='z',s=20, depthshade=True, color=color_test, marker='*')
    #     plt.title("SVM Classifier")
    #     ax.set_xlabel('Retweets axis')
    #     ax.set_ylabel('Favorites axis')
    #     ax.set_zlabel('Z axis')
    #     ax.view_init(azim=-70,elev=10)
    #     ax.legend(loc=2)
    #     plt.show()


if __name__ == "__main__":
    print("You are in main")
