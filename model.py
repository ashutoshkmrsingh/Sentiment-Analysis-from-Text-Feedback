# importing required libraries
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from autocorrect import Speller
from textblob import TextBlob
from expand import Expander
from statistics import mean


class Model:
    """
    Model to check polarity, named entity recognition and subjectivity of the sentence.
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")  # loading model
        self.sentences = 'You are awesome'  # default review
        self.domain = 'Mobile'  # default domain
        self.e = Expander()  # text expander object
        self.spell = Speller(lang='en')  # English language spell checker
        self.sent_analyzer = SentimentIntensityAnalyzer()  # object of sentence polarity analyzer
        self.result = []  # result of review
        self.subjectivity = []  # subjectivity of each sentence
        self.positive_sentiment = []  # list of positive sentiment
        self.negative_sentiment = []  # list of negative sentiment
        self.neutral_sentiment = []  # list of neutral sentiment

    def input(self, review, domain):
        """
        :param review: review text as input
        :param domain: and its domain
        :return: None
        """
        def reset(self):
            self.result = []
            self.subjectivity = []
            self.positive_sentiment = []
            self.negative_sentiment = []
            self.neutral_sentiment = []

        reset(self)
        self.e.input(review)
        self.sentences = self.spell(self.e.expanded_sentence).replace('. ', ', ')
        self.sentences = self.sentences.split(', ')

        self.domain = domain
        self.process()

    def process(self):
        """
        Process the review
        :return: None
        """
        for sent in self.sentences:
            local_list = []
            doc = self.nlp(sent)

            local_list.append(sent)

            polarity = self.sent_analyzer.polarity_scores(sent)  # polarity of the sentence
            if polarity['neg'] == 0.0:
                polarity['neu'] /= 3
                polarity['pos'] += polarity['neu'] * 2
            elif polarity['pos'] == 0.0:
                polarity['neu'] /= 3
                polarity['neg'] += polarity['neu'] * 2
            local_list.append(polarity)
            self.positive_sentiment.append(polarity['pos'])
            self.negative_sentiment.append(polarity['neg'])
            self.neutral_sentiment.append(polarity['neu'])

            local_list.append(TextBlob(sent).sentiment[1])  # subjectivity of the sentence
            self.subjectivity.append(TextBlob(sent).sentiment[1])

            # identifying noun and noun chunks
            d = {}
            for chunk in doc.noun_chunks:
                d['chunk'] = chunk.text
                d['chunk_root'] = chunk.root.text
                d['chunk_root_type'] = chunk.root.dep_
            local_list.append(d)

            self.result.append(local_list)

    def output(self):
        """
        return the result of the text
        :return: result list
        """
        return self.result

    def overall_polarity(self):
        """
        overall result of the sentence
        :return: dictionary as {'subjectivity' : 1.0, 'neg' : 1.0, 'neu' : 1.0, 'pos' : 1.0}
        """
        d = {}
        d['subjectivity'] = mean(self.subjectivity)
        d['neg'] = mean(self.negative_sentiment)
        d['neu'] = mean(self.neutral_sentiment)
        d['pos'] = mean(self.positive_sentiment)
        return d


