import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import requests
from PIL import Image
from io import BytesIO
from gtts import gTTS
import os
import gradio as gr

# Function to record audio (optional if users upload files directly)
def record_audio(duration=5):
    fs = 44100  # Sample rate
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()  # Wait for the recording to finish
    filename = "output.wav"
    wav.write(filename, fs, recording)
    print(f"Recording saved as {filename}")
    return filename

# Function to convert voice to text
def voice_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        print("Processing audio...")
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Text:", text)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"

# Function to fetch an image from Unsplash
def fetch_image(query):
    access_key = "20ZSk4jYNHS4JF-oJuLOao3W8ouK7jmZRhEJkysimsw"  # Replace with your Unsplash API key
    url = f"https://api.unsplash.com/search/photos?query={query}&client_id={access_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            image_url = data["results"][0]["urls"]["regular"]
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            return img
    return None

# Function to generate speech from text
def generate_speech(text):
    tts = gTTS(text)
    speech_filename = "speech.mp3"
    tts.save(speech_filename)
    os.system(f"start {speech_filename}")  # Play the speech on Windows
    return speech_filename

# Gradio interface function
def process_audio(audio_file):
    # Convert audio to text
    text = voice_to_text(audio_file)
    if not text or "Could not" in text:
        return "Failed to process audio.", None

    # Fetch an image based on the text
    image = fetch_image(text)
    if image:
        image.save("output_image.jpg")
    else:
        return text, None

    # Return text and image
    return text, image

# Gradio app
interface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(sources=["microphone"], type="filepath"),  # Corrected to use sources
    outputs=[
        gr.Textbox(label="Transcribed Text"),
        gr.Image(label="Generated Image"),
    ],
    title="Audio to Text/Image App",
    description="Speak into your microphone. The app transcribes the audio to text, fetches an image based on the text, and generates speech.",
)

# Launch the app
if __name__ == "__main__":
    interface.launch( )
