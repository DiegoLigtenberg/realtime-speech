from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor, pipeline
from pydub import AudioSegment
import whisper
from settings import MODEL_PARSER
from pytube import YouTube
import os
import glob
import time
import streamlit as st
import subprocess

class BagOfModels:
    '''model            ->  is a model from hugging face
       model_names      ->  modelnames that can be chosen from in streamlit
       model_settinsg   ->  settings of model that can be customized by user
       model_tasks      ->  the task that the model is doing (text-to-speech, summarization)
    '''
    # class variables
    args = MODEL_PARSER

    def __init__(self,model,model_names,model_settings,model_tasks, **kwargs):
        self.model = model
        self.model_names = model_names
        self.model_settings = model_settings
        self.model_tasks = model_tasks
        self.kwargs = kwargs

    @classmethod
    def get_model_settings(cls):
        bag_of_models = BagOfModels(**vars(cls.args))
        return bag_of_models.model_settings
    
    @classmethod
    def get_model_names(cls):
        bag_of_models = BagOfModels(**vars(cls.args))
        return bag_of_models.model_names
    
    @classmethod
    def get_model(cls):
        bag_of_models = BagOfModels(**vars(cls.args))
        return bag_of_models.model

    @classmethod
    def get_model_tasks(cls):
        bag_of_models = BagOfModels(**vars(cls.args))
        return bag_of_models.model_tasks
        
    @classmethod
    def load_model(cls,model_name,**kwargs):           
        bag_of_models = BagOfModels(**vars(cls.args))
        cls.model = bag_of_models.model
        assert model_name in bag_of_models.model_names, f"please pick one of the available models: {bag_of_models.model_names}"      
        return Model(model_name,**cls.model[model_name])
     
    
class Model:
    def __init__(self,model_name,task,url,**kwargs):
        self.url = url
        self.model_name = model_name
        self.name = self.url.split("https://huggingface.co/")[1] 
        self.task = task
        self.kwargs = kwargs      
        self.init_optional_args(**self.kwargs)    
    
    def init_optional_args(self,year=None,description=None):
        self._year = year
        self._description = description
    
    @st.cache_data
    def load_cached_whisper(self):
        model = whisper.load_model(self.model_name.split("_")[1]) #tiny - base - medium 
        return model

    def predict_stt(self,source,source_type,model_task):       
        model = self.load_cached_whisper()
        stt = SoundToText(source,source_type,model_task,model=model,tokenizer=None)
        # stt.whisper()
        return stt

    # TODO if more summarization models are implemented, add them here
    def predict_summary(self):
        tokenizer = Wav2Vec2Processor.from_pretrained(self.name)
        model = Wav2Vec2ForCTC.from_pretrained(self.name) # Note: PyTorch Model

class SoundToText():
    def __init__(self,source,source_type,model_task,model,tokenizer=None):
        self.source = source
        self.source_type = source_type
        self.model = model
        self.model_task = model_task
        self.tokenizer = tokenizer
    
    # not yet implemented
    def wav2vec(self,size):
        pass
    
    # not yet implemented
    def wav2vec2(self,size):
        pass

    def whisper(self):
        # download youtube url
        self.timestr = time.strftime("%Y%m%d-%H%M%S")
        if self.source_type == "YouTube":       
            self.audio_path = YouTube(self.source).streams.get_by_itag(140).download("output/", filename=f"audio{self.timestr}") 
        
        # convert file to audiosegment
        if self.source_type == "File": 
            audio = None
            if self.source.name.endswith('.wav'): audio = AudioSegment.from_wav(self.source)
            elif self.source.name.endswith('.mp3'): audio = AudioSegment.from_mp3(self.source)  
            elif self.source.name.endswith(".m4a"):   audio = AudioSegment.from_file(self.source,format='m4a'); audio.set_channels(1); audio.set_frame_rate(16000)    

            audio.export(f'output/audio{self.timestr}.wav', format='wav')
            self.audio_path = f"output/audio{self.timestr}.wav"   
        
        # transcribe the model and extract text, language, and time-annotated segments
        self.raw_output = self.model.transcribe(self.audio_path,verbose=True,fp16=False) #float point 16 not supported for cpu
        self.text = self.raw_output["text"]
        self.language = self.raw_output["language"]
        self.segments = self.raw_output["segments"]

        # Remove token ids from the output
        for segment in self.segments:
            del segment["tokens"]

        # source is transcribed
        self.transcribed = True
    
    def clear_folder(self):
        os.remove(f'output/audio{self.timestr}')
    
    def clear_all(self):
        dir = 'output'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
             
class TextToSummary():
    
    def __init__(self,input_text,min_length,max_length):        
        self.summarizer = self.load_summary_model()
        self.summary_input = input_text   
        self.summary_output = (self.summarizer(self.summary_input, min_length=min_length, max_length=max_length, do_sample=False))
    
    def load_summary_model(self):
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn") #facebook/bart-large-cnn
        return summarizer
        
    def get_summary(self):
        return self.summary_output
        
    def wav2vec(self):
        pass

# debugging
if __name__== "__main__":
    args = MODEL_PARSER
    models = BagOfModels.get_model_names()
    tasks = BagOfModels.get_model_tasks()
    whisper_base = BagOfModels.load_model("whisper_base",**vars(args))
    whisper_base.predict_stt()