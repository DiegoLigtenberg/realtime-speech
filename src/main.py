import streamlit as st
from models import BagOfModels, SoundToText, TextToSummary
from settings import MODEL_PARSER
import os.path
from os import path

args = MODEL_PARSER

st.set_page_config(
    page_title="TTS Applications | Incore Solutions",
    layout="wide",
    menu_items={
        "About": """This is a simple GUI for OpenAI's Whisper.""",
    },
)

def open_instructions():
    with open("instructions.md", "r") as f:
        st.write(f.read())



# Render input type selection on the sidebar & the form
input_type = st.sidebar.selectbox("Input Type", ["YouTube", "File"])



with st.sidebar.form("input_form"):
    submitted = False
    if input_type == "YouTube":
        youtube_url = st.text_input("Youtube URL (shorter than 8 minutes)")       
    elif input_type == "File":
        input_file = st.file_uploader("File", type=["mp3", "wav"])       

    # whisper_model = st.selectbox("Whisper model", options = [whisper for whisper in BagOfModels.get_model_names() if "whisper" in whisper] , index=1) 
    whisper_model = st.selectbox("Whisper model", options = ["whisper_tiny"]) 

    # summary = st.checkbox("summarize")
    # if summary:
        
    min_sum = st.number_input("Number of words in the summary", min_value=1, step=10,value=50)
    # max_sum = st.number_input("Maximum words in the summary", min_value=2, step=10,value=50)
    max_sum = min_sum
    min_sum = min(min_sum,max_sum)
    
    
    # submitted = st.form_submit_button(label="Save settings")
    if submitted:
        st.write("settings saved")
    
# with st.sidebar.form("save settings"):
    transcribe = st.form_submit_button(label="Transcribe!")
   
# if input_type == "YouTube":
#      st.title("Youtube to Summary converter ")

if transcribe:

    # remove app if it is already running
    path = "output"
    if not os.path.exists(path):
        os.makedirs(path)
    dir = 'output'
    if len(os.listdir(dir)) > 1:  # removes audio files if someone else was using app or duplicate audio files because bug
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f)) 
        

    if input_type == "YouTube":
        if youtube_url and youtube_url.startswith("http"):
            model = BagOfModels.load_model(whisper_model,**vars(args))
            st.session_state.transcription = model.predict_stt(source=youtube_url,source_type=input_type,model_task="stt")
        else:
            st.error("Please enter a valid YouTube URL")
            open_instructions()
        
    elif input_type == "File":
        if input_file:
            model = BagOfModels.load_model(whisper_model,**vars(args))
            st.session_state.transcription = model.predict_stt(source=input_file,source_type=input_type,model_task="stt")
        else:
            st.error("Please upload a file")


if "transcription" in st.session_state and transcribe:
    st.session_state.transcription.whisper() # -> it is already running in models.py
    # if not path.exists("output/audio/"):

    # create two columns to separate page and youtube video
    transcription_col, media_col = st.columns(2, gap="large")

    transcription_col.markdown("#### Audio")
    try:
        with open(st.session_state.transcription.audio_path, "rb") as f:
            transcription_col.audio(f.read())
        transcription_col.markdown("---")
        transcription_col.markdown(f"#### Transcription (whisper model - `{whisper_model}`)")
        transcription_col.markdown(f"##### Language: `{st.session_state.transcription.language}`")

        # Trim raw transcribed output off tokens to simplify
        raw_output = transcription_col.expander("Raw output")
        raw_output.markdown(st.session_state.transcription.raw_output["text"])

        # st.write(min_sum)
        # if summary:
        summarized_output = transcription_col.expander("summarized output")
        # CURRENTLY ONLY SUPPORTS 1024 WORD TOKENS -> TODO: FIND METHOD TO INCREASE SUMMARY FOR LONGER VIDS -> 1024 * 4 = aprox 800 words within 1024 range
        text_summary = TextToSummary(str(st.session_state.transcription.text[:1024*4]),min_sum,max_sum).get_summary()
        summarized_output.markdown(text_summary[0]["summary_text"])    

        # Show transcription in format with timers added to text
        time_annotated_output = transcription_col.expander("time_annotated_output")
        for segment in st.session_state.transcription.segments:
            time_annotated_output.markdown(
                f"""[{round(segment["start"], 1)} - {round(segment["end"], 1)}] - {segment["text"]}"""
            )

        # Show input youtube video
        if input_type == "YouTube":
            media_col.markdown("---")
            media_col.markdown("#### Original YouTube Video")
            media_col.video(st.session_state.transcription.source)
        transcribe = False
        # clear folder of audio files
        st.session_state.transcription.transcribed = True
        st.session_state.transcription.clear_folder()

    except:
        # bugg with multiusers and not deleting audio file TODO
        st.session_state.transcription.clear_all()
        transcribe = False

else:
    transcribe = False 

# else:
#     # bugg with multiusers and not deleting audio file 
#     st.session_state.transcription.clear_all()

