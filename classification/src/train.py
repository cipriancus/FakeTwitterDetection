from pyspark import SparkContext
import src.config as cfg
import src.processing as prp
import src.algorithms.SVM as svm
import src.algorithms.NB as nb
import time
import src.algorithms.RandomForest as rf

cfg.dir

testing_file_location = 'Test_feature_extracted.csv'
training_file_location = 'Training_feature_extracted.csv'

if __name__ == "__main__":
    spark_context = SparkContext("local","Twitter");

    start_time = time.time()

    ###############################################################################
    training_data = prp.PreProcessing('../data/RawTrainingDataSet.csv', 'Training')
    training_data.process()

    test_data = prp.PreProcessing('../data/RawTestDataSet.csv', 'Test')
    test_data.process()
    ###############################################################################

    ##############################SVM##############################################
    svm_time = time.time()

    svm_classifier = svm.SVMClassifier(training_file_location,spark_context)
    svm_predict_test_data_class = svm_classifier.classify_testdata(testing_file_location)
    accuracy_svm = svm_classifier.confusion_matrix(svm_predict_test_data_class)

    print("SVM EXECUTION TIME " + str(time.time() - svm_time))
    ##############################################################################

    ##############################NB###############################################
    nb_time = time.time()

    nb_classifier = nb.NbClassifier(training_file_location,spark_context)
    nb_predict_test_data_class = nb_classifier.classify_testdata(testing_file_location)
    accuracy_nb = nb_classifier.confusion_matrix(nb_predict_test_data_class)

    print("NB EXECUTION TIME " + str(time.time() - nb_time))
    ##############################################################################

    ##############################RF###############################################
    rf_time = time.time()

    rf_classifier = rf.RFClassifier(training_file_location, spark_context)
    rf_predict_test_data_class = rf_classifier.classify_testdata(testing_file_location)
    accuracy_rf = rf_classifier.confusion_matrix(rf_predict_test_data_class)

    print("RF EXECUTION TIME " + str(time.time() - rf_time))
    ##############################################################################
    print("Total Execution time is " + str(time.time() - start_time))
