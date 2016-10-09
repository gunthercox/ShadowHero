from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from textblob.classifiers import NaiveBayesClassifier
from itertools import chain
import pickle
import os
import codecs

PICKLE_FILE = 'classifier_pickle.pickle'

current_directory = os.path.dirname(os.path.abspath(__file__))
pickle_file_path = os.path.join(current_directory, PICKLE_FILE)

if os.path.isfile(pickle_file_path):
    classifier = pickle.load(pickle_file_path)
else:
    data_directory = os.path.join(current_directory, 'TwitterClassifier', 'data')

    good_corpus_path = os.path.join(data_directory, 'good_corpus.txt')
    bad_corpus_path = os.path.join(data_directory, 'bad_corpus.txt')

    good_training_data = [(line, 0) for line in open(good_corpus_path, encoding='utf8') if not line.startswith('#')]
    bad_training_data = [(line, 1) for line in codecs.open(bad_corpus_path, 'r', encoding='utf-8', errors='ignore') if not line.startswith('#')]

    training_data = chain(good_training_data, bad_training_data)

    classifier = NaiveBayesClassifier(training_data)

    with open(pickle_file_path, 'wb') as handle:
        pickle.dump(classifier, handle)

print(classifier.classify('I hate you so much'))
print(classifier.classify('I love your hair style'))


'''
Cases:

# General insults

In the case where a user is issuing general insults towards others

Response: ShadowHero will tell the user to calm down or take it easy.
This action brings awareness to the situation and may help to diffuse it.

# Repeated attacks on a user: Verbally defend the user and flag the abuser's account.

# Direct message the user and ask if they are being attacked.
Use this data to 'learn' about perceptions of harassment.
'''

class AntiHarassmentLogic(LogicAdapter):

    def __init__(self, **kwargs):
        super(AntiHarassmentLogic, self).__init__(kwargs)

    def can_process(self, statement):
        return True

    def process(self, statement):

        confidence = 0
        statement = Statement("")

        return confidence, statement