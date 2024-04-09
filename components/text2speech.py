from gtts import gTTS

class TTS:
    def generate(self, sentences, filepath):
        text = "\n".join(sentences)
        tts = gTTS(text)
        tts.save(filepath)
