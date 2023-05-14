from pydub import AudioSegment
import os

# Load the MP3 file
audio_file = AudioSegment.from_file("D:/Users/Diego Ligtenberg/Downloads/Opname (4).mp3", format="mp3")
# Set the desired output bitrate (in kbps)
output_bitrate = "64k"

# Reduce the audio quality to make it smaller
audio_file = audio_file.set_frame_rate(16000).set_channels(1)

# Export the compressed audio as a new MP3 file
compressed_file = "compressed_audio.mp3"
audio_file.export(compressed_file, format="mp3", bitrate=output_bitrate)

# Check the size of the compressed file
if os.path.getsize(compressed_file) > 25000000:
    print("Error: Compressed file is still too large")
else:
    print("Compressed file created successfully!")