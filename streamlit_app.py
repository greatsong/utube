import streamlit as st
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

def download_video_and_audio(youtube_url, output_path):
    try:
        yt = YouTube(youtube_url)
        
        # Download video
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_file_path = video_stream.download(output_path=output_path)

        # Extract audio
        audio_clip = AudioFileClip(video_file_path)
        audio_file_path = os.path.join(output_path, f"{yt.title}.mp3")
        audio_clip.write_audiofile(audio_file_path)
        audio_clip.close()

        return video_file_path, audio_file_path
    except Exception as e:
        st.error(f"Error: {e}")
        return None, None

# Streamlit app
st.title("YouTube Downloader")
st.write("Enter a YouTube URL to download its video and audio.")

youtube_url = st.text_input("YouTube URL:", "")
output_path = "downloads"  # Directory to save downloads
os.makedirs(output_path, exist_ok=True)

if st.button("Download"):
    if youtube_url:
        video_path, audio_path = download_video_and_audio(youtube_url, output_path)
        if video_path and audio_path:
            st.success("Download complete!")
            with open(video_path, "rb") as video_file:
                st.download_button(label="Download Video", data=video_file, file_name=os.path.basename(video_path))
            with open(audio_path, "rb") as audio_file:
                st.download_button(label="Download Audio", data=audio_file, file_name=os.path.basename(audio_path))
    else:
        st.warning("Please enter a valid YouTube URL.")
