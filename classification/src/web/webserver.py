from flask import Flask, request
from src.processing import *
from src.algorithms.SVM import SVMClassifier
import numpy as np

app = Flask(__name__)

training_file_location = 'Training_feature_extracted.csv'
preprocessing = PreProcessing()
svmClassifier = SVMClassifier(training_file_location)


@app.route("/classification", methods=['POST'])
def classification():
    tweet = {key: str(value) for key, value in request.values.items()}
    #print(tweet)
    processed_tweet = preprocessing.process_tweet(tweet)
    #print(processed_tweet)
    value_to_classify = np.array([float(value) for value in processed_tweet.values()]).reshape(1, 3)
    #print(value_to_classify)
    output = svmClassifier.classify(value_to_classify)

    return "Spam" if output == 1 else "Not Spam"


if __name__ == "__main__":
    app.run(debug=True)
