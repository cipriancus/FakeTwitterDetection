import src.config as cfg
import src.processing as prp
import src.algorithms.SVM as svm
import src.algorithms.KNN as knn
import src.algorithms.NB as nb

cfg.dir

testing_file_location = 'Test_feature_extracted.csv'
training_file_location = 'Training_feature_extracted.csv'

if __name__ == "__main__":
    ###############################################################################
    training_data = prp.PreProcessing('../data/RawTrainingDataSet.csv', 'Training')
    training_data.process()

    test_data = prp.PreProcessing('../data/RawTestDataSet.csv', 'Test')
    test_data.process()
    ###############################################################################

    ##############################SVM##############################################

    svm_classifier = svm.SVMClassifier(training_file_location)
    svm_predict_test_data_class = svm_classifier.classify_testdata(testing_file_location)
    accuracy_svm = svm_classifier.confusion_matrix(svm_predict_test_data_class)
    svm_classifier.plot()

    ##############################################################################

    ##############################KNN##############################################

    knn_classifier = knn.KNNClassifier(training_file_location)
    knn_predict_test_data_class = knn_classifier.classify_testdata(testing_file_location)
    accuracy_knn = knn_classifier.confusion_matrix(knn_predict_test_data_class)
    knn_classifier.plot()

    ##############################################################################

  ##############################NB###############################################

    nb_classifier = nb.NbClassifier(training_file_location)
    nb_predict_test_data_class = nb_classifier.classify_testdata(testing_file_location)
    accuracy_nb = nb_classifier.confusion_matrix(nb_predict_test_data_class)
    nb_classifier.plot()

    ##############################################################################

