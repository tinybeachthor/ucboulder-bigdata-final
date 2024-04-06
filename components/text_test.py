from .text import TextUtil

util = TextUtil()

def test_split_sentences():
    text = "One. Two. Three."
    output = util.split_sentences(text)
    assert len(output) == 3

def test_split_sentences_single():
    text = "One."
    output = util.split_sentences(text)
    assert len(output) == 1
    text = "One"
    output = util.split_sentences(text)
    assert len(output) == 1

def test_split_sentences_empty():
    text = ""
    output = util.split_sentences(text)
    assert len(output) == 0
