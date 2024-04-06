import nltk

class TextUtil:
    def __init__(self):
        nltk.download('punkt')

    def split_sentences(self, text):
        sentences = nltk.sent_tokenize(text)
        return sentences
