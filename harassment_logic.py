from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.utils.clean import clean_whitespace
from textblob.classifiers import NaiveBayesClassifier
from itertools import chain
import pickle
import os
import re
import codecs
import random


class AntiHarassmentLogic(LogicAdapter):
    """
    A logic analysis class designed to determine if an input statement
    contains text that qualifies as harassment and return a response
    as needed based on that analysis.
    """

    def __init__(self, **kwargs):
        super(AntiHarassmentLogic, self).__init__(**kwargs)

        self.callouts = [
            'Hey, take it easy.'
        ]

        PICKLE_FILE = 'small_classifier_pickle.pickle'

        current_directory = os.path.dirname(os.path.abspath(__file__))
        pickle_file_path = os.path.join(current_directory, PICKLE_FILE)

        if os.path.isfile(pickle_file_path):
            with open(pickle_file_path, 'rb') as handle:
                self.classifier = pickle.load(handle)
        else:
            data_directory = os.path.join(current_directory, 'TwitterClassifier', 'data')

            good_corpus_path = os.path.join(data_directory, 'good_corpus_small.txt')
            bad_corpus_path = os.path.join(data_directory, 'bad_corpus_small.txt')

            good_training_data = [(self.clean_text(line), 1, ) for line in open(good_corpus_path, 'rU', encoding='utf8') if line.strip() and not line.startswith('#')]
            bad_training_data = [(self.clean_text(line), 0, ) for line in codecs.open(bad_corpus_path, 'rU', encoding='utf-8', errors='ignore') if line.strip() and not line.startswith('#')]

            training_data = list(good_training_data) + list(bad_training_data)

            self.classifier = NaiveBayesClassifier(training_data)

            with open(pickle_file_path, 'wb') as handle:
                pickle.dump(self.classifier, handle)

    def clean_text(self, text):
        # Remove user mentions
        text = re.sub(r'@\S+', '', text)

        # Remove extre whitespace
        text = clean_whitespace(text)

        # Return the lowercase text
        return text.lower()

    def can_process(self, statement):
        return True

    def process(self, statement):
        confidence = self.classifier.classify(statement.text)

        text = random.choice(self.callouts)
        response_statement = Statement(text)

        return confidence, response_statement
