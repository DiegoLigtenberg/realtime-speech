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

# Set up the Stripe API key
# # Set up the Stripe API key
# stripe.api_key = "sk_test_51MVOv5R8hJO9C6jw9bPYOYcjZJlzI2cCEgetlVbq9NjH4qa8PbypMwPMGRG1WNSdCtnPcP5NyuZHEgWQYxOfnZIk00DV2ewgjZ"
# stripe.api_key = "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"

# Create a form to collect the payment information
# name = st.text_input("Name")
# email = st.text_input("Email")
# amount = 5 #st.number_input("Amount")

# When the user submits the form, create a payment intent and generate a payment URL
# if st.button("Submit"):
#     intent = stripe.PaymentIntent.create(
#         amount=int(amount * 100),
#         currency="usd",
#         metadata={"name": name, "email": email},
#     )
#     payment_url = intent["charges"]["data"][0]["payment_method_details"]["url"]
#     st.write("Please complete your payment at", payment_url)
user_has_payed = False
if user_has_payed == False:
    text_input_container = st.empty()
    t = text_input_container.text_input("password")

    if  t == "XAIR#9373":
        text_input_container.empty()
        st.info(t)
        user_has_payed = True
    else:
        st.write("https://buy.stripe.com/9AQ7wwexT2U8gwg6op")
        st.error("""We kindly ask for a small one-time payment of 10 euros to keep this app running (see link above).   
        This one-time fee will help us maintain the app and provide ongoing support to our users.   
        Thank you for your understanding and support!""")
        
        if len(t)>0:        
            st.error("""Incorrect password.    
            get the password by paying a one-time fee to keep this app running""")



if user_has_payed:
    password = st.empty()
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