'''
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import speech_recognition as sr
import io
from pydub import AudioSegment
import librosa
import whisper
from scipy.io import wavfile
from test import record_voice

model = Wav2Vec2ForCTC.from_pretrained(r'yongjian/wav2vec2-large-a') # Note: PyTorch Model
tokenizer = Wav2Vec2Processor.from_pretrained(r'yongjian/wav2vec2-large-a')


r = sr.Recognizer()

from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

with sr.Microphone(sample_rate=16000) as source:
    print("You can start speaking now")
    record_voice()
    # x,_ = librosa.load("output.wav")
    # model_inputs = tokenizer(x, sampling_rate=16000, return_tensors="pt", padding=True)
    # logits = model(model_inputs.input_values, attention_mask=model_inputs.attention_mask).logits.cuda() # use .cuda() for GPU acceleration
    # pred_ids = torch.argmax(logits, dim=-1).cpu()
    # pred_text = tokenizer.batch_decode(pred_ids)
    # # print(x[:10],x.shape)
    # print('Transcription:', pred_text)

    
    model = whisper.load_model("base")
   
    result = model.transcribe("output.wav",verbose=True)
    print(result["text"])
    segments = (result["segments"])

    print(segments)
    for segment in segments:
        del segment["tokens"]
        print(f"""[{round(segment["start"], 1)} - {round(segment["end"], 1)}] - {segment["text"]}""")

    

    summary_input = result["text"]
   
    summary_output = (summarizer(summary_input, max_length=30, min_length=20, do_sample=False))
    print(summary_output)
    with open("raw_text.txt",'w',encoding = 'utf-8') as f:
        f.write(summary_input)
        f.close()
    with open("summary_text.txt",'w',encoding = 'utf-8') as f:
        f.write(summary_output[0]["summary_text"])
        f.close()

'''