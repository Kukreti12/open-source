import io
import IPython.display as ipd
import grpc
import riva.client

auth = riva.client.Auth(uri='10.10.162.12:50051')

riva_asr = riva.client.ASRService(auth)
# This example uses a .wav file with LINEAR_PCM encoding.
# read in an audio file from local disk
path = "NVIDIA AI\mono.wav" 
with io.open(path, 'rb') as fh:
    content = fh.read()
ipd.Audio(path)

# Set up an offline/batch recognition request
config = riva.client.RecognitionConfig()
config.language_code = "en-US"                    # Language code of the audio clip
config.max_alternatives = 1                       # How many top-N hypotheses to return
config.enable_automatic_punctuation = True        # Add punctuation when end of VAD detected
config.audio_channel_count = 1                    
response = riva_asr.offline_recognize(content, config)
asr_best_transcript = response.results[0].alternatives[0].transcript

print("\n\nFull Response Message:")
print(type(response.results[-1]))
print(response.results[-1])

