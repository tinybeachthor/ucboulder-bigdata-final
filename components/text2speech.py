from gtts import gTTS

class TTS:
    def generate(self, sentences, filepath):
        text = " ".join(sentences)
        tts = gTTS(text)
        tts.save(filepath)
