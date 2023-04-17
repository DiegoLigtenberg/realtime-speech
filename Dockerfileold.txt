# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.8
# [27-10 16:00] Erik Willems
FROM jrottenberg/ffmpeg:4.1-ubuntu


#TODO pip install 
#TODO python install 
#TODO Ubuntu update
RUN apt-get -y update
RUN apt-get -y install

# installing pip3 & python 3
RUN apt install -y python3-pip --upgrade
RUN apt install -y python3



# RUN python3 -m pip install PEP517



EXPOSE 8501

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
# RUN  pip install ffmpeg-python
RUN apt-get -y install git
RUN python3 -m pip install git+https://github.com/openai/whisper.git

WORKDIR /app
COPY . /app
ADD . /src
# COPY requirements.txt .
# RUN apt-get  update
# RUN apt-get -y install libasound-dev libportaudio2 libportaudiocpp0 portaudio19-dev -y
# RUN pip install -y --upgrade pip
# RUN python3 -m pip install pyaudio
# RUN apt-get update \
#         && apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev libasound-dev libsndfile1-dev -y \
#         && pip3 install pyaudio
# RUN python3 -m pip install streamlit-webrtc

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run"]

CMD ["./src/main.py"]
