def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        decrypted_char = chr((ord(char) - shift) % 128)
        decrypted_text += decrypted_char
    return decrypted_text

# from pyannote.audio import Pipeline
# pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
#                                     use_auth_token="ACCESS_TOKEN_GOES_HERE")


# # apply the pipeline to an audio file
# diarization = pipeline("audio.wav")

# # dump the diarization output to disk using RTTM format
# with open("audio.rttm", "w") as rttm:
#     diarization.write_rttm(rttm)