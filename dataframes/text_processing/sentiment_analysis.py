# NLTK for traditional approach
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
import nltk.sentiment.vader as sev

# math
import numpy as np
import pandas as pd


class SentimentAnalysis:
    def __init__(self, comments):
        """
        receives a list of comments and performs a sentiment analysis on each sentence
        it uses the stock market lexicon by Nuno Oliveira for the sentiment polarity scores
        :param comments:
        """
        self.comments = comments  # these will be passed in list format from the main class
        self.master_dict = pd.read_csv("resources/Loughran-McDonald_MasterDictionary_1993-2021.csv")
        self.stocklex = pd.read_csv("resources/Nuno_Oliveira_Stock_Lexicon.csv",
                                    sep=",",
                                    decimal=".")
        self.stock_symbols = pd.read_csv("resources/nasdaq_screener_1667058131530.csv")["Symbol"].values
        self.sia = sev.SentimentIntensityAnalyzer()

    def return_polarity_score(self, sentence, type):
        """
        :param sentence: sentence in string format
        :param type: either nltk or stocklex
        :return: float value between -1.0 and 1.0
        """
        if type == "nltk":
            return self.sia.polarity_scores(sentence)["compound"]
        elif type == "stocklex":
            return self.get_stock_lex_val(sentence)

    def get_stock_lex_val(self, sentence):
        """
        receives a sentence, tokenizes it into unigrams and bigrams
        then it will iterate over the list of bigrams and check if they can be found in the stock lexicon
        if yes, the value will be stored
        and the individual tokens of the bigram will be added to a list of tokens to ignore
        another iteration will be performed on the list of unigrams,
        where all unigrams that are in the ignore list will be ignored
        for those that make it, the respective value will be stored too
        :param sentence: sentence in string format
        :return: the mean of each token's values
        """
        values = []   # list of values of bigrams/unigrams
        data = self.stocklex
        tokens = self.tokenize(sentence)   # tokenize sentence
        tokens = self.apply_tags(tokens)   # apply NUM und tkr tags
        bigrams = self._bigrams(tokens)   # extract bigrams
        ignore = []   # bigrams whose value has been extracted

        for bigram in bigrams:
            if bigram in data['Item'].values:
                score = data.loc[data['Item'] == bigram, 'Aff_Score'].item()
                values.append(score)
                ignore.append(bigram)

        for token in tokens:
            if token not in '\t'.join(ignore) and token not in stopwords.words():
                if token in data['Item'].values:
                    try:
                        score = data.loc[data['Item'] == token, 'Aff_Score'].item()
                        values.append(score)
                        ignore.append(token)
                    except ValueError:
                        pass

        return np.mean(values) if values != [] else 0   # return 0 if no token with an assigned value was found

    def apply_tags(self, tokens):
        """
        the stock market sentiment lexicon uses tags for certain types of items
        so this method applies those tags, specifically numbers will be replaced with "NUM"
        and stock symbols will be replaced with "tkr"
        :param tokens: list of tokens
        :return: list of tokens with tags applied
        """
        for i, token in enumerate(tokens):
            if token.isnumeric():
                tokens[i] = "NUM"
            if token.upper() in self.stock_symbols:
                tokens[i] = "tkr"
        return tokens

    def _bigrams(self, tokens):
        """ creates list of bigrams for a sentence """
        list_of_bigrams = []
        for i, token in enumerate(tokens):
            if i < len(tokens)-1:
                bigram_lst = [token, tokens[i + 1]]
                bigram = " ".join(bigram_lst)
                list_of_bigrams.append(bigram)
        return list_of_bigrams

    def tokenize(self, comment):
        """ tokenizes a sentence into words """
        tokens = word_tokenize(comment)
        return tokens

    def sentenize(self, comment):
        """ tokenizes a comment into sentences """
        return nltk.sent_tokenize(comment)

    def get_pos_tag(self, token):
        """ gets the POS tag of a token """
        tup = nltk.pos_tag([token])
        return tup[0][1]

    def _get_mean_score(self):
        """
        helper method
        iterates over each comment, turns it into a list of sentences and gets the mean sentiment for each sentence
        that value will be appended to the "total" list
        which will be returned and received by the get_men_score() method
        """
        total = []
        for comment in self.comments:
            sentences = self.sentenize(comment)
            for sentence in sentences:
                total.append(self.return_polarity_score(sentence, type="nltk"))
        return total

    def get_mean_score(self):
        """
        gets a list of sentiment scores from _get_mean_score() and calculates the mean
        if more than 0 comments have been analyzed, return the mean value
        else return 0 (not NUN)
        """
        total = self._get_mean_score()
        result = float(np.round(np.mean(total), 5))
        return result if len(self.comments) > 0 else 0  # get mean score for list of comments, if no comments return 0

