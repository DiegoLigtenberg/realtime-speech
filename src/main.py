import streamlit as st
from models import BagOfModels, SoundToText, TextToSummary
from settings import MODEL_PARSER
import os.path
from io import BytesIO
from datetime import datetime
import numpy as np
from PIL import Image
import random

from encryption import caesar_decrypt
# check https://dashboard.stripe.com/products/prod_NjneJRpeYKWVDR
#^GOX)?9=9
#^GOX)9769
#^GOX);879
#^GOX)=;87
#^GOX)98<?

args = MODEL_PARSER

dir = 'output'

st.set_page_config(
    page_title="TTS Applications | XairEU",
    layout="wide",
    menu_items={
        "About": """This is a GUI for the Transcription App using Whisper as a Machine Learning backbone.""",
    },
    initial_sidebar_state="expanded",
    
)

def open_instructions():
    with open("instructions.md", "r") as f:
        st.write(f.read())
    
# make audio outputfile
def add_audio_configuration():
    path = "output"
    if not os.path.exists(path):
        os.makedirs(path)
    
link_list = ["https://buy.stripe.com/9AQ7wwexT2U8gwg6op",
             "https://buy.stripe.com/bIY7ww4XjfGUcg05km",
             "https://buy.stripe.com/7sIg329dzbqE2Fq4gj",
             "https://buy.stripe.com/fZe8AAfBX66k4NyeUY",
             "https://buy.stripe.com/7sI9EE2PbfGU3Ju4gl"]
im_list = ["example/qr_code_transparent1.png",
           "example/qr_code_transparent2.png",
           "example/qr_code_transparent3.png",
           "example/qr_code_transparent4.png",
           "example/qr_code_transparent5.png"
           ]
rng = random.randint(0,4) # included 0 and 4
link = link_list[rng]
im = im_list[rng]

# @st.cache_data
def myfunction():
    return False
user_has_payed = myfunction()
st.markdown("### Audio Transcription WebApp")
placeholder = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()
placeholder4 = st.empty()
placeholder5 = st.empty()
image = Image.open(im)
placeholder_im = st.empty()

placeholder6 = st.empty()

production = False
if user_has_payed == False:
    placeholder.markdown("""We're excited to offer you a powerful tool that can transcribe audio data and YouTube videos using state-of-the-art machine learning algorithms.   
    With this app, you can easily transcribe audio files in popular formats such as .wav and .mp3, and also transcribe audio from non-copyrighted YouTube videos.   
    """)
    placeholder2.markdown("""؜
    
    Usecases include: 
    - Transcription of (recorded) meetings
    - Transcription of (school) interviews 
    - Transcription of online lectures

    """
    )
    placeholder_im.image(image,width=128, caption="",use_column_width=False)
    
    
    text_input_container = st.empty()
    placeholder5.error(f"""We kindly ask for a [one-time payment]({link}) of €10,- to keep this app running (see link below).   
        Payment of the fee unlocks the passsword required to acces the Transcription App.   
        PLEASE ENSURE TO SAVE THE PASSWORD AS IT WILL ONLY BE VISIBLE ONCE AFTER PURCHASE!   
        ؜   
        Thank you for your understanding and support!""")

    t = text_input_container.text_input("Password (available after purchase using link above, make sure to SAVE it)")
    
    try:
        if  t == os.environ["PASS_1"] or t == os.environ["PASS_2"] or t == os.environ["PASS_3"] or t == os.environ["PASS_4"] or t == os.environ["PASS_5"]:
            text_input_container.empty()
            st.info(t)
            user_has_payed = True
            # production is only true if correct pass is filled in
            production = True
    except: 
        # local = true       
        pass
        
        
    
    if t == "GOX)?": # master key
        text_input_container.empty()
        st.info(t)
        user_has_payed = True
    elif t ==  caesar_decrypt("^GOX)?9=9",len(dir)) and not production:
        text_input_container.empty()
        st.info(t)
        user_has_payed = True

    else:
        if not production:
            if len(t)>0:        
                st.error("""Incorrect password.    
                get the password by paying a one-time fee to keep this app running""")
                st.write("forgot password? email to:")
                st.write("xairservice@gmail.com")
            for i in range(3):
                st.write(" ")
            col2, _ = st.columns(2, gap="large")
            col2.markdown("### Example Transcription of audio file")
            with st.expander(""):
                with open("./example/example_interview.mp3", "rb") as audio_file:
                    audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mpeg')

                with open("./example/transcribe_example.txt", "r") as f:
                    file_contents = f.readlines()
                    
                    col, _ = st.columns(2, gap="large")
                    for line in file_contents:
                        col.markdown(line)
            




if user_has_payed:
    # Render input type selection on the sidebar & the form
    input_type = st.sidebar.selectbox("Input Type", ["YouTube", "File"])
    password = st.empty()

    placeholder_im.empty()
    placeholder.empty()
    placeholder2.empty()
    placeholder5.empty()
    placeholder6.empty()
    placeholder3.markdown("""**Explanation Controlls**؜
    
    
    Input type\t:     Refers to the user's selected input for transcription, either a YouTube video URL or an uploaded audio file in .mp3 or .wav format.    
    Whisper model\t:     The user-selected transcription model, with larger models providing higher accuracy but longer processing times.   
    Transcribe\t:     The user-initiated transcription process, with automatic display of results upon completion.    
                   \t      Processing time varies based on file length and selected model.
    Download text\t:     User action to download the transcribed text as a .txt file after completion for local storage.
    
    """ 
    )

    with st.sidebar.form("input_form"):
        if input_type == "YouTube":
            youtube_url = st.text_input("Youtube URL (shorter than 8 minutes)")       
        elif input_type == "File":
            input_file = st.file_uploader("File", type=["mp3","wav","m4a"])       

        if production:
            whisper_model = st.selectbox("Whisper model", options = [whisper for whisper in BagOfModels.get_model_names() if "whisper" in whisper and not "large" in whisper and not "medium"  in whisper] , index=1) 
        else:
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
            placeholder4.markdown("<h2 style='text-align: center;'>Please wait till the program is finished (max 10 minutes)</h2>.",unsafe_allow_html=True)
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
            # st.experimental_rerun()
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

            # this triggers once!
            if not transcribe:
                placeholder2.empty()
                placeholder3.empty()
                placeholder4.empty()
                filename = "transcribe.txt"                
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
                    label="Download Text File",
                    data=buffer,
                    file_name=filename,
                    mime=file_extension,
                )
                os.remove(filename)
            

        except Exception as e:
            st.write("traffic of this app migh be high, please wait a minute and try again")
            st.write(e)
        st.session_state.transcription.clear_all()




    else:
        # removes audio files if someone else was using app or duplicate audio files because bug
        if len(os.listdir(dir)) > 1:  
            for f in os.listdir(dir):
                os.remove(os.path.join(dir, f)) 