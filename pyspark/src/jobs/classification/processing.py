from string import whitespace
import csv
from collections import defaultdict

columns_header = ['Date', 'Tweet_Text', 'Tweet_Id', 'User_Id', 'User_Name', 'User_Screen_Name', 'Retweets', 'Favorites',
                  'Class']


class PreProcessing(object):

    def __init__(self, file_name=None, file_type=None):
        self.file_name = file_name
        self.type = file_type

        try:
            import os
            print(os.getcwd())
            spam_name = 'spam_words.csv'
            spam_header = "words"
            self.spam_data = ''

            self.spam_data = self.read_csv(spam_name)[spam_header]

        except Exception as e:
            print(e)

        try:
            swear_name = 'swear.csv'
            swear_header = "swear"
            self.swear_data = ''

            self.swear_data = self.read_csv(swear_name)[swear_header]

        except Exception as e:
            print(e)

    def read_csv(self, file_name):
        columns = defaultdict(list)  # each value in each column is appended to a list

        with open(file_name) as f:
            reader = csv.DictReader(f)  # read rows into a dictionary format
            for row in reader:  # read a row as {column1: value1, column2: value2,...}
                for (k, v) in row.items():  # go over each column name and value
                    columns[k].append(v)  # append the value into the appropriate list# based on column name k\
        return columns

    def write_csv(self, file_name, data, collums=None):

        new_collums = list()
        new_values = list()
        for k, v in data.items():
            if (collums != None and k in collums) or collums == None:
                new_collums.append(k)
                new_values.append(v)

        row = list(zip(*new_values))

        with open(file_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(new_collums)
            for iterator in row:
                if '' not in iterator:
                    writer.writerow(iterator)

    def process(self):
        try:
            import os
            self.Data_preprocessed_file = self.read_csv(self.file_name)
        except (FileNotFoundError, FileExistsError, MemoryError) as e:
            print("file is not in correct format")
            print(e)

        try:
            prefix = '_Cleaned.csv'
            file = self.type + prefix
            self.write_csv(file, self.Data_preprocessed_file)
        except PermissionError as e:
            print("file is opened by someone, please rerun after closing the file")
            print(e)

        self.Data_preprocessed_file['Date'] = [PreProcessing.process_date_lambda(value) for value in
                                               self.Data_preprocessed_file['Date']]

        self.Data_preprocessed_file['Tweet_Text'] = self.Data_preprocessed_file['Tweet_Text']

        self.Data_preprocessed_file['Tweet_length'] = [len(value.translate(str.maketrans('', '', whitespace))) for value
                                                       in self.Data_preprocessed_file['Tweet_Text']]

        self.Data_preprocessed_file['Number_of_URL'] = [value.count('http*') for value in
                                                        self.Data_preprocessed_file['Tweet_Text']]

        self.Data_preprocessed_file['No_of_arond_word'] = [value.count('@') for value in
                                                           self.Data_preprocessed_file['Tweet_Text']]

        self.Data_preprocessed_file['No_of_hash_word'] = [value.count('#') for value in
                                                          self.Data_preprocessed_file['Tweet_Text']]

        self.Data_preprocessed_file['Length_of_User_Name'] = [len(value) for value in
                                                              self.Data_preprocessed_file['User_Screen_Name']]

        self.Data_preprocessed_file['Number_of_Spam_Word'] = [
            PreProcessing.spam_word_count_lambda(value.split(' '), self.spam_data) for value in
            self.Data_preprocessed_file['Tweet_Text']]

        self.Data_preprocessed_file['Number_of_Swear_Word'] = [
            PreProcessing.swear_word_count_lambda(value.split(' '), self.swear_data) for value in
            self.Data_preprocessed_file['Tweet_Text']]

        self.Data_preprocessed_file['New_Feature'] = self.Data_preprocessed_file['No_of_hash_word'] + \
                                                     self.Data_preprocessed_file['No_of_arond_word'] + \
                                                     self.Data_preprocessed_file['Number_of_URL'] + \
                                                     self.Data_preprocessed_file['Number_of_Swear_Word'] + \
                                                     self.Data_preprocessed_file['Number_of_Spam_Word']

        try:
            prefix_pre = '_feature_selected.csv'
            file_name = self.type + prefix_pre
            self.write_csv(file_name, self.Data_preprocessed_file)
        except PermissionError:
            print("file is opened by someone, please rerun after closing the file")

        header = ["Retweets", "Favorites", "New_Feature", "Class"]
        try:
            prefix = '_feature_extracted.csv'
            file_name = self.type + prefix
            self.write_csv(file_name, self.Data_preprocessed_file, header)
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
    training = PreProcessing('../data/training_dataset.csv', 'Training')
    training.process()
    test = PreProcessing('../data/test_dataset.csv', 'Test')
    test.process()
