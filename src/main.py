import streamlit as st
from models import BagOfModels, SoundToText, TextToSummary
from settings import MODEL_PARSER
import os.path
from os import path
from io import BytesIO
from datetime import datetime
args = MODEL_PARSER

dir = 'output'

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
    
# make audio outputfile
def add_audio_configuration():
    path = "output"
    if not os.path.exists(path):
        os.makedirs(path)
    



# Render input type selection on the sidebar & the form
input_type = st.sidebar.selectbox("Input Type", ["YouTube", "File"])

if st.button("Download text file"):
            
    filename = "transcribe.txt"
    if os.path.exists(filename):
        file_extension = ".txt"
        with open(filename, "r") as f:
            file_contents = f.read()
        file_bytes = file_contents.encode('utf-8')
        # Create a BytesIO object
        buffer = BytesIO()
        buffer.write(file_bytes)
        # Set the cursor at the beginning of the buffer
        buffer.seek(0)
        # Display the download button
        st.download_button(
            label="Download",
            data=buffer,
            file_name=filename,
            mime=file_extension,
        )
        os.remove(filename)
    else:
        st.write("please first transcribe before downloading text file")

with st.sidebar.form("input_form"):
    if input_type == "YouTube":
        youtube_url = st.text_input("Youtube URL (shorter than 8 minutes)")       
    elif input_type == "File":
        input_file = st.file_uploader("File", type=["mp3", "wav"])       

    whisper_model = st.selectbox("Whisper model", options = [whisper for whisper in BagOfModels.get_model_names() if "whisper" in whisper] , index=1) 
    # whisper_model = st.selectbox("Whisper model", options = ["whisper_tiny"]) 
    
    # # let the user select amout of words in the summary
    # min_sum = st.number_input("Number of words in the summary", min_value=1, step=10,value=50)
    # # max_sum = st.number_input("Maximum words in the summary", min_value=2, step=10,value=50)
    # max_sum = min_sum
    # min_sum = min(min_sum,max_sum)
    
    add_audio_configuration()
    transcribe = st.form_submit_button(label="Transcribe!")

    # removes audio files if someone else was using app or duplicate audio files because bug
    if len(os.listdir(dir)) > 0:  
        transcribe = False
        st.write("you only have to click once")
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f)) 
    

if transcribe:
    # select song using Youtube
    if input_type == "YouTube":
        if youtube_url and youtube_url.startswith("http"):
            model = BagOfModels.load_model(whisper_model,**vars(args))
            st.session_state.transcription = model.predict_stt(source=youtube_url,source_type=input_type,model_task="stt")
        else:
            st.error("Please enter a valid YouTube URL")
            open_instructions()
    
    # select song using personal file (mp3 or wav supports)
    elif input_type == "File":
        if input_file:
            model = BagOfModels.load_model(whisper_model,**vars(args))
            st.session_state.transcription = model.predict_stt(source=input_file,source_type=input_type,model_task="stt")
        else:
            st.error("Please upload a file")


if "transcription" in st.session_state and transcribe:
    try:
        # enables whisper to transcribe
        st.session_state.transcription.whisper()

        # create two columns to separate page and youtube video
        transcription_col, media_col = st.columns(2, gap="large")

        transcription_col.markdown("#### Audio")    
        with open(st.session_state.transcription.audio_path, "rb") as f:
            transcription_col.audio(f.read())
        transcription_col.markdown("---")
        transcription_col.markdown(f"#### Transcription (whisper model - `{whisper_model}`)")
        transcription_col.markdown(f"##### Language: `{st.session_state.transcription.language}`")

        # Trim raw transcribed output off tokens to simplify
        raw_output = transcription_col.expander("Raw output")
        raw_output.markdown(st.session_state.transcription.raw_output["text"])
        with open ("transcribe.txt",'w',encoding="utf-8") as t:
            text = str(st.session_state.transcription.raw_output["text"])
            for segment in st.session_state.transcription.segments:
                time_objs = datetime.fromtimestamp(segment["start"])
                time_obje = datetime.fromtimestamp(segment["end"])
                time_objs = time_objs.strftime("%M:%S.%f")[:-4]
                time_obje = time_obje.strftime("%M:%S.%f")[:-4]
                # st.write(time_obje)
                text = f"""[{time_objs} --> {time_obje}] - {segment["text"]}\n"""
                t.write(text)
            
        # # if summary:
        # summarized_output = transcription_col.expander("summarized output")
        # # CURRENTLY ONLY SUPPORTS 1024 WORD TOKENS -> TODO: FIND METHOD TO INCREASE SUMMARY FOR LONGER VIDS -> 1024 * 4 = aprox 800 words within 1024 range
        # text_summary = TextToSummary(str(st.session_state.transcription.text[:1024*4]),min_sum,max_sum).get_summary()
        # summarized_output.markdown(text_summary[0]["summary_text"])    

        # # Show transcription in format with timers added to text
        # time_annotated_output = transcription_col.expander("time_annotated_output")
        # for segment in st.session_state.transcription.segments:
        #     time_annotated_output.markdown(
        #         f"""[{round(segment["start"], 1)} - {round(segment["end"], 1)}] - {segment["text"]}"""
        #     )

                # Create a button to download the text file

        # Show input youtube video
        if input_type == "YouTube":
            media_col.markdown("---")
            media_col.markdown("#### Original YouTube Video")
            media_col.video(st.session_state.transcription.source)
        transcribe = False

        # clear folder of audio files
        st.session_state.transcription.transcribed = True

    except Exception as e:
        st.write("traffic of this app migh be high, please wait a minute and try again")
        st.write(e)
    st.session_state.transcription.clear_all()




else:
    # removes audio files if someone else was using app or duplicate audio files because bug
    if len(os.listdir(dir)) > 1:  
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f)) 