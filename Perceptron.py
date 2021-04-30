from __future__ import division
from __future__ import print_function
import os
import sys
import collections
import re
import copy
import ast


class Document:
    text = ""
    true_class = ""
    learned_class = ""

    word_freqs = {}

    def __init__(self, text, counter, true_class):
        self.text = text
        self.word_freqs = counter
        self.true_class = true_class

    def Text(self):
        return self.text

    def WordFreqs(self):
        return self.word_freqs

    def getTrueClass(self):
        return self.true_class

    def getLearnedClass(self):
        return self.learned_class

    def setLearnedClass(self, prediction):
        self.learned_class = prediction


def buildData(storage_dict, directory, true_class):
    for dir_entry in os.listdir(directory):
        dir_entry_path = os.path.join(directory, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as text_file:
                text = text_file.read()
                storage_dict.update({dir_entry_path: Document(text, bagOfWords(text), true_class)})


def bagOfWords(text):
    bagsofwords = collections.Counter(re.findall(r'\w+', text))
    return dict(bagsofwords)


def DataVocabulary(data_set):
    vocabulary = []
    for i in data_set:
        for j in data_set[i].WordFreqs():
            if j not in vocabulary:
                vocabulary.append(j)
    return vocabulary


def FilterStopWords(stop_words, data_set):
    filtered_data = copy.deepcopy(data_set)
    for i in stop_words:
        for j in filtered_data:
            if i in filtered_data[j].WordFreqs():
                del filtered_data[j].WordFreqs()[i]
    return filtered_data


def perceptronClassifier(weights, classes, instance):
    weight_sum = weights['init_weight']
    for i in instance.WordFreqs():
        if i not in weights:
            weights[i] = 0.0
        weight_sum += weights[i] * instance.WordFreqs()[i]
    if weight_sum > 0:
        return 1
    else:
        return 0


def setPerceptronWeights(weights, learning_constant, spam_ham_training_set, num_iterations, classes):
    for i in num_iterations:
        for d in spam_ham_training_set:
            weight_sum = weights['init_weight']
            for f in spam_ham_training_set[d].WordFreqs():
                if f not in weights:
                    weights[f] = 0.0
                weight_sum += weights[f] * spam_ham_training_set[d].WordFreqs()[f]
            perceptron_output = 0.0
            if weight_sum > 0:
                perceptron_output = 1.0
            target_value = 0.0
            if spam_ham_training_set[d].getTrueClass() == classes[1]:
                target_value = 1.0
            for w in spam_ham_training_set[d].WordFreqs():
                weights[w] += float(learning_constant) * float((target_value - perceptron_output)) * float(
                    spam_ham_training_set[d].WordFreqs()[w])


def main():
    args = str(sys.argv)
    args = ast.literal_eval(args)

    if (len(args) < 3):

        print("You have input less than the minimum number of arguments.")
        print("Usage: python Perceptron.py  <no-of-iterations> <learning-constant>")


    else:

        iterations = args[1]
        learning_constant = args[2]

        spam_ham_training_set = {}
        spam_ham_test_set = {}
        filtered_spam_ham_training_set = {}
        filtered_spam_ham_test_set = {}

        classes = ["ham", "spam"]

        stop_words = []
        with open('/home/sshetty9/ML/Data/stopwords.txt', 'r') as txt:
            stop_words = (txt.read().splitlines())

        buildData(spam_ham_training_set, "/home/sshetty9/ML/Data/train" + "/spam", classes[1])
        buildData(spam_ham_training_set, "/home/sshetty9/ML/Data/train" + "/ham", classes[0])
        buildData(spam_ham_test_set, "/home/sshetty9/ML/Data/test" + "/spam", classes[1])
        buildData(spam_ham_test_set, "/home/sshetty9/ML/Data/test" + "/ham", classes[0])

        filtered_spam_ham_training_set = FilterStopWords(stop_words, spam_ham_training_set)
        filtered_spam_ham_test_set = FilterStopWords(stop_words, spam_ham_test_set)

        vocabulary_spam_ham_training_set = DataVocabulary(spam_ham_training_set)
        filtered_vocalbulary_spam_ham_training_set = DataVocabulary(filtered_spam_ham_training_set)

        weights = {'init_weight': 1.0}
        filtered_weights = {'init_weight': 1.0}
        for i in vocabulary_spam_ham_training_set:
            weights[i] = 0.0
        for i in filtered_vocalbulary_spam_ham_training_set:
            filtered_weights[i] = 0.0

        setPerceptronWeights(weights, learning_constant, spam_ham_training_set, iterations, classes)
        setPerceptronWeights(filtered_weights, learning_constant, filtered_spam_ham_training_set, iterations, classes)

        correct_predictions = 0
        for i in spam_ham_test_set:
            prediction = perceptronClassifier(weights, classes, spam_ham_test_set[i])
            if prediction == 1:
                spam_ham_test_set[i].setLearnedClass(classes[1])
                if spam_ham_test_set[i].getTrueClass() == spam_ham_test_set[i].getLearnedClass():
                    correct_predictions += 1

            if prediction == 0:
                spam_ham_test_set[i].setLearnedClass(classes[0])
                if spam_ham_test_set[i].getTrueClass() == spam_ham_test_set[i].getLearnedClass():
                    correct_predictions += 1

        filtered_correct_predictions = 0
        for i in filtered_spam_ham_test_set:
            prediction = perceptronClassifier(filtered_weights, classes, filtered_spam_ham_test_set[i])
            if prediction == 1:
                filtered_spam_ham_test_set[i].setLearnedClass(classes[1])
                if filtered_spam_ham_test_set[i].getTrueClass() == filtered_spam_ham_test_set[i].getLearnedClass():
                    filtered_correct_predictions += 1

            if prediction == 0:
                filtered_spam_ham_test_set[i].setLearnedClass(classes[0])
                if filtered_spam_ham_test_set[i].getTrueClass() == filtered_spam_ham_test_set[i].getLearnedClass():
                    filtered_correct_predictions += 1

        print("Learning constant: %.4f" % float(learning_constant))
        print("Number of iterations: %d" % int(iterations))
        print("................................................\n")
        print("Emails classified correctly: %d/%d" % (correct_predictions, len(spam_ham_test_set)))
        print( "Accuracy before filtering: %.4f%%" % (float(correct_predictions) / float(len(spam_ham_test_set)) * 100.0))
        print("Filtered emails classified correctly: %d/%d" % (filtered_correct_predictions, len(filtered_spam_ham_test_set)))
        print("Filtered accuracy: %.4f%%" % ( float(filtered_correct_predictions) / float(len(filtered_spam_ham_test_set)) * 100.0))



if __name__ == '__main__':
    main()