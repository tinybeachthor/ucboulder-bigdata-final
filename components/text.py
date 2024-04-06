import nltk

nltk.download('punkt')

def split_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences
