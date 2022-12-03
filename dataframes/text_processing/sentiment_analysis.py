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
        self.comments = comments  # these will be passed in list format from the main class
        self.volume = self.get_post_volume()
        self.master_dict = pd.read_csv("resources/Loughran-McDonald_MasterDictionary_1993-2021.csv")
        self.stocklex = pd.read_csv("resources/Nuno_Oliveira_Stock_Lexicon.csv",
                                    sep=",",
                                    decimal=".")
        self.stock_symbols = pd.read_csv("resources/nasdaq_screener_1667058131530.csv")["Symbol"].values
        self.sia = sev.SentimentIntensityAnalyzer()

    def return_polarity_score(self, sentence, type):
        if type == "nltk":
            return self.sia.polarity_scores(sentence)["compound"]
        elif type == "stocklex":
            return self.get_stock_lex_val(sentence)

    def get_stock_lex_val(self, sentence):
        values = []
        data = self.stocklex
        tokens = self.tokenize(sentence)
        tokens = self.apply_tags(tokens)
        bigrams = self._bigrams(tokens)
        ignore = []
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
                        values.append(self.sia.polarity_scores(token)["compound"])
                else:
                    values.append(self.sia.polarity_scores(token)["compound"])

        return np.mean(values) if values != [] else 0

    def apply_tags(self, tokens):
        # the stock market sentiment lexicon uses tags for certain types of items
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
        tokens = word_tokenize(comment)
        return tokens

    def sentenize(self, comment):
        return nltk.sent_tokenize(comment)

    def get_pos_tag(self, token):
        tup = nltk.pos_tag([token])
        return tup[0][1]

    def _get_mean_score(self):
        total = []
        for comment in self.comments:
            sentences = self.sentenize(comment)
            for sentence in sentences:
                total.append(self.return_polarity_score(sentence, type="stocklex"))
        return total

    def get_mean_score(self):
        total = self._get_mean_score()
        result = float(np.round(np.mean(total), 5))
        return result if self.volume > 0 else 0  # get mean score for list of comments, if no comments return 0

    def get_post_volume(self):
        return len(self.comments)
