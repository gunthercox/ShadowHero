# -*- coding: utf-8 -*-
from chatterbot.adapters.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.utils.clean import clean_whitespace
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import nltk.classify.util
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

        PICKLE_FILE = 'classifier_pickle.pickle'

        current_directory = os.path.dirname(os.path.abspath(__file__))
        pickle_file_path = os.path.join(current_directory, PICKLE_FILE)

        if os.path.isfile(pickle_file_path):
            self.logger.info(u'Using cached classifier data')
            with open(pickle_file_path, 'rb') as handle:
                self.classifier = pickle.load(handle)
        else:
            self.logger.info(u'Generating classifier data')

            data_directory = os.path.join(current_directory, 'TwitterClassifier', 'data')

            good_corpus_path = os.path.join(data_directory, 'good_corpus_small.txt')
            bad_corpus_path = os.path.join(data_directory, 'bad_corpus_small.txt')

            negative_features = []
            with codecs.open(bad_corpus_path, 'r', encoding='utf-8', errors='ignore') as bad_file:
                for line in bad_file:
                    if not line.startswith('#') and line.strip():
                        line = self.clean_text(line)
                        negative_features.append((self.word_feats(line.split()), 1, ))

            positive_features = []
            with open(good_corpus_path, 'r', encoding='utf8') as good_file:
                for line in good_file:
                    if not line.startswith('#') and line.strip():
                        line = self.clean_text(line)
                        posfeats.append((self.word_feats(line.split()), 0, ))

            training_features = positive_features + posfeats

            self.classifier = NaiveBayesClassifier.train(training_features)

            with open(pickle_file_path, 'wb') as handle:
                pickle.dump(self.classifier, handle)

        self.classifier.show_most_informative_features(20)

    def word_feats(self, words):
        return dict([(word, True) for word in words if len(word) > 3])

    def remove_punctuation(self, text):
        exclude = r'~.,!`*%&-+=:;{}[]<>#/|\?$£@'
        text = ''.join(c for c in text if c not in exclude)
        return text

    def clean_text(self, text):
        # Remove user mentions
        text = re.sub(r'@\S+', '', text)

        text = self.remove_punctuation(text)

        # Remove extre whitespace
        text = clean_whitespace(text)

        # Return the lowercase text
        return text.lower()

    def process(self, statement):
        clean_text = self.clean_text(statement.text)
        features = {word.lower(): (word in word_tokenize(clean_text)) for word in clean_text.split()}
        confidence = self.classifier.classify(features)

        # Allow additional response triggers
        if any(s in clean_text.split() for s in ['stupid', 'hate', 'dumb']):
            confidence = 1

        text = random.choice(self.callouts)
        response_statement = Statement(text)

        self.logger.info(u'Responding to {} with a confidence of {}'.format(
            statement.text, confidence
        ))

        return confidence, response_statement
