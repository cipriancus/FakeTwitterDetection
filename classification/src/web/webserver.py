from flask import Flask, request
from src.processing import *
from src.algorithms.SVM import SVMClassifier
from pyspark import SparkContext

app = Flask(__name__)

training_file_location = 'Training_feature_extracted.csv'
preprocessing = PreProcessing()
spark_context = SparkContext("local", "Twitter");
svmClassifier = SVMClassifier(training_file_location,spark_context)


@app.route("/classification", methods=['POST'])
def classification():
    tweet = {key: str(value) for key, value in request.values.items()}
    processed_tweet = preprocessing.process_tweet(tweet)
    output = svmClassifier.classify(processed_tweet)

    return "Spam" if output == 1 else "Not Spam"


if __name__ == "__main__":
    app.run(debug=True)
