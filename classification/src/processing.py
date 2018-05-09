import warnings
from string import whitespace

import src.config as cfg
import pandas as pd


cfg.dir
pd.set_option('display.max_colwidth', 30000)
columns_header = ['Date', 'Tweet_Text', 'Tweet_Id', 'User_Id', 'User_Name', 'User_Screen_Name', 'Retweets', 'Favorites',
                  'Class']


class PreProcessing(object):

    def __init__(self, file_name=None, file_type=None):
        self.file_name = file_name
        self.type = file_type

        try:
            file_name = '../data/spam_words.csv'
            spam_header = ["words"]
            self.spam_data = ''

            raw_file = pd.read_csv(file_name, sep=',', usecols=spam_header, index_col=None, quoting=3,
                                   encoding='utf-8')
            self.spam_data = raw_file.dropna(subset=spam_header)
        except (FileNotFoundError, FileExistsError, MemoryError) as e:
            print("file is not in correct format")
            print(e)

        try:
            swear_name = '../data/swear.csv'
            swear_header = ["swear"]
            self.swear_data = ''

            raw_file = pd.read_csv(swear_name, sep=',', usecols=swear_header, index_col=None, quoting=3,
                                   encoding='utf-8')
            self.swear_data = raw_file.dropna(subset=swear_header)
        except (FileNotFoundError, FileExistsError, MemoryError) as e:
            print("file is not in correct format")
            print(e)

    def process(self):

        try:
            raw_file = pd.read_csv(self.file_name, sep=',', usecols=columns_header, index_col=None, quoting=3,
                                   encoding='utf-8')
            self.Data_preprocessed_file = raw_file.dropna(subset=columns_header)
        except (FileNotFoundError, FileExistsError, MemoryError) as e:
            print("file is not in correct format")
            print(e)

        try:
            prefix = '_Cleaned.csv'
            file = self.type + prefix
            self.Data_preprocessed_file.to_csv(file, header=None, sep=',', index=False)
        except PermissionError as e:
            print("file is opened by someone, please rerun after closing the file")
            print(e)

        self.Data_preprocessed_file['Date'] = self.Data_preprocessed_file['Date'].astype(str)
        try:
            self.Data_preprocessed_file['Date'] = self.Data_preprocessed_file['Date'] \
                .map(lambda x: PreProcessing.process_date_lambda(x))

        except(TypeError, SyntaxError, SystemExit, SyntaxWarning) as e:
            print("Check the data in a file")

        try:
            self.Data_preprocessed_file = self.Data_preprocessed_file.sort_values(by='Date')

        except ValueError:
            print("Values are not in date format")

        self.Data_preprocessed_file = self.Data_preprocessed_file[
            (self.Data_preprocessed_file['Date'] > '2011-07-31 23:59:59') & (
                    self.Data_preprocessed_file['Date'] < '2011-08-30 00:00:00')]
        self.Data_preprocessed_file['Tweet_Text'] = self.Data_preprocessed_file['Tweet_Text'].astype(str)
        self.Data_preprocessed_file['Tweet_length'] = self.Data_preprocessed_file['Tweet_Text'].map(
            lambda x: len(x.translate(str.maketrans('', '', whitespace))))
        self.Data_preprocessed_file['Number_of_URL'] = self.Data_preprocessed_file['Tweet_Text'].map(
            lambda x: x.count('http*'))
        self.Data_preprocessed_file['No_of_arond_word'] = self.Data_preprocessed_file['Tweet_Text'].map(
            lambda x: x.count('@'))
        self.Data_preprocessed_file['No_of_hash_word'] = self.Data_preprocessed_file['Tweet_Text'].map(
            lambda x: x.count('#'))
        self.Data_preprocessed_file['Length_of_User_Name'] = self.Data_preprocessed_file['User_Screen_Name'].map(
            lambda x: len(str(x)))

        self.Data_preprocessed_file['Number_of_Spam_Word'] = self.Data_preprocessed_file['Tweet_Text'].map(
            lambda x: PreProcessing.spam_word_count_lambda(x.split(' '), self.spam_data))

        self.Data_preprocessed_file['Number_of_Swear_Word'] = self.Data_preprocessed_file['Tweet_Text'].map(
            lambda x: PreProcessing.swear_word_count_lambda(x.split(' '), self.swear_data))
        self.Data_preprocessed_file['New_Feature'] = self.Data_preprocessed_file['No_of_hash_word'] + \
                                                     self.Data_preprocessed_file['No_of_arond_word'] + \
                                                     self.Data_preprocessed_file['Number_of_URL'] + \
                                                     self.Data_preprocessed_file['Number_of_Swear_Word'] + \
                                                     self.Data_preprocessed_file['Number_of_Spam_Word']

        try:
            prefix_pre = '_feature_selected.csv'
            file_name = self.type + prefix_pre
            self.Data_preprocessed_file.to_csv(file_name, sep=',', index=False)
        except PermissionError:
            print("file is opened by someone, please rerun after closing the file")

        # def feature_extraction(self, type):

        header = ["Retweets", "Favorites", "New_Feature", "Class"]
        try:
            prefix = '_feature_extracted.csv'
            file_name = self.type + prefix
            self.Data_preprocessed_file.to_csv(file_name, columns=header, sep=',', index=False)
        except PermissionError:
            print("file is opened by someone, please rerun after closing the file")

    def process_tweet(self, tweet: dict) -> dict:
        process_data = dict(tweet)
        process_data['Date'] = PreProcessing.process_date_lambda(tweet['Date'])
        process_data['Tweet_Text'] = tweet['Tweet_Text']
        process_data['Tweet_length'] = len(tweet["Tweet_Text"].translate(str.maketrans('', '', whitespace)))
        process_data['Number_of_URL'] = tweet['Tweet_Text'].count('http*')
        process_data['No_of_arond_word'] = tweet['Tweet_Text'].count('@')
        process_data['No_of_hash_word'] = tweet['Tweet_Text'].count('#')
        process_data['Length_of_User_Name'] = len(str(tweet['User_Screen_Name']))
        process_data['Number_of_Spam_Word'] = PreProcessing.spam_word_count_lambda(tweet['Tweet_Text'].split(' '),
                                                                                   self.spam_data)
        process_data['Number_of_Swear_Word'] = PreProcessing.swear_word_count_lambda(tweet['Tweet_Text'].split(' '),
                                                                                     self.swear_data)
        process_data['New_Feature'] = process_data['No_of_hash_word'] + \
                                      process_data['No_of_arond_word'] + \
                                      process_data['Number_of_URL'] + \
                                      process_data['Number_of_Swear_Word'] + \
                                      process_data['Number_of_Spam_Word']

        header = ["Retweets", "Favorites", "New_Feature", ]
        processed_data = dict(zip(header, [process_data[key] for key in header]))
        return processed_data

    @staticmethod
    def process_date_lambda(x):
        try:
            return x[x.find("[") + 1: x.find("]") - 1]
        except (ValueError, SyntaxError) as e:
            print("Check the data in a file")
            print(e)

    @staticmethod
    def spam_word_count_lambda(word, data):

        spam_count = {}
        spam_list = data
        for i in spam_list:
            try:
                spam_count[i] = word.count(i)
            except ValueError:
                print("Cant find the word list as a parameter")
        return sum(spam_count.values())

    @staticmethod
    def swear_word_count_lambda(word, swear_data):
        swear_count = {}
        swear_list = swear_data
        for i in swear_list:
            try:
                swear_count[i] = word.count(i)
            except ValueError:
                print("Cant find the word list as a parameter")
        return sum(swear_count.values())


if __name__ == "__main__":
    training = PreProcessing('../data/RawTrainingDataSet.csv', 'Training')
    training.process()
    test = PreProcessing('../data/RawTestDataSet.csv', 'Test')
    test.process()
