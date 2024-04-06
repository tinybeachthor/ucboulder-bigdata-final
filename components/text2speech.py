from transformers import AutoProcessor, BarkModel
import scipy
import numpy as np

# quarter second of silence
SILENCE = np.zeros(int(0.25 * sample_rate))

class TTS:
    def __init__(self, voice_preset="v2/en_speaker_9"):
        self.processor = AutoProcessor.from_pretrained("suno/bark-small")
        self.model = BarkModel.from_pretrained("suno/bark-small")
        self.sample_rate = model.generation_config.sample_rate
        self.voice_preset = voice_preset

    def generate(self, sentences, filepath):
        pieces = []
        for sentence in sentences:
            inputs = self.processor(s, voice_preset=self.voice_preset)
            audio_array = self.model.generate(**inputs)
            audio_array = audio_array.cpu().numpy().squeeze()
            pieces += [audio_array, SILENCE.copy()]

        audio = np.concatenate(pieces)
        scipy.io.wavfile.write(filepath, rate=self.sample_rate, data=audio)
