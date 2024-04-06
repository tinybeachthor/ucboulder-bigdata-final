from .text import split_sentences

def test_split_sentences():
    text = "One. Two. Three."
    output = split_sentences(text)
    assert len(output) == 3

def test_split_sentences_single():
    text = "One."
    output = split_sentences(text)
    assert len(output) == 1
    text = "One"
    output = split_sentences(text)
    assert len(output) == 1

def test_split_sentences_empty():
    text = ""
    output = split_sentences(text)
    assert len(output) == 0
