from transformers import AutoProcessor, BarkModel
import nltk
import scipy
import numpy as np

nltk.download('punkt')

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained("suno/bark-small")

voice_preset = "v2/en_speaker_9"
sample_rate = model.generation_config.sample_rate

silence = np.zeros(int(0.25 * sample_rate))  # quarter second of silence

title = "Impact of Electron-Electron Cusp on Configuration Interaction Energies"
summary = """
The effect of the electron-electron cusp on the convergence of configuration interaction (CI) wave functions is examined. By analogy with the pseudopotential approach for electron-ion interactions, an effective electron-electron interaction is developed which closely reproduces the scattering of the Coulomb interaction but is smooth and finite at zero electron-electron separation. The exact many-electron wave function for this smooth effective interaction has no cusp at zero electron-electron separation. We perform CI and quantum Monte Carlo calculations for He and Be atoms, both with the Coulomb electron-electron interaction and with the smooth effective electron-electron interaction. We find that convergence of the CI expansion of the wave function for the smooth electron-electron interaction is not significantly improved compared with that for the divergent Coulomb interaction for energy differences on the order of 1 mHartree. This shows that, contrary to popular belief, description of the electron-electron cusp is not a limiting factor, to within chemical accuracy, for CI calculations.
"""

sentences = nltk.sent_tokenize(summary)

pieces = []
for s in sentences:
    print(s)
    print('')

    inputs = processor(s, voice_preset=voice_preset)
    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()

    pieces += [audio_array, silence.copy()]

audio = np.concatenate(pieces)

scipy.io.wavfile.write("test.wav", rate=sample_rate, data=audio)
