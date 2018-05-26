import time
from . import processing as prp
from .algorithms import SVM as svm
from .algorithms import NB as nb
from .algorithms import RandomForest as rf

__author__ = 'ciprianc'


def analyze(sc):
    testing_file_location = 'Test_feature_extracted.csv'
    training_file_location = 'Training_feature_extracted.csv'

    start_time = time.time()

    ###############################################################################
    training_data = prp.PreProcessing('training_dataset.csv', 'Training')
    training_data.process()

    test_data = prp.PreProcessing('test_dataset.csv', 'Test')
    test_data.process()
    ###############################################################################

    ##############################SVM##############################################
    svm_time = time.time()

    svm_classifier = svm.SVMClassifier(training_file_location, sc)
    svm_predict_test_data_class = svm_classifier.classify_testdata(testing_file_location)
    # accuracy_svm = svm_classifier.confusion_matrix(svm_predict_test_data_class)
    print("SVM EXECUTION TIME " + str(time.time() - svm_time))
    ##############################################################################

    ##############################RF###############################################
    rf_time = time.time()

    rf_classifier = rf.RFClassifier(training_file_location, sc)
    rf_predict_test_data_class = rf_classifier.classify_testdata(testing_file_location)
    # accuracy_rf = rf_classifier.confusion_matrix(rf_predict_test_data_class)

    print("RF EXECUTION TIME " + str(time.time() - rf_time))
    ##############################################################################

    ##############################NB###############################################
    nb_time = time.time()

    nb_classifier = nb.NbClassifier(training_file_location, sc)
    nb_predict_test_data_class = nb_classifier.classify_testdata(testing_file_location)
    # accuracy_nb = nb_classifier.confusion_matrix(nb_predict_test_data_class)
    print("NB EXECUTION TIME " + str(time.time() - nb_time))
    ##############################################################################

    print("Total Execution time is " + str(time.time() - start_time))

    return time.time() - start_time