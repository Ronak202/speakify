import pyttsx3
import gradio as gr

def text_to_audio_pyttsx3(text):
    """Converts text to audio using pyttsx3 with a female voice."""
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties like speech rate and volume
    engine.setProperty("rate", 150)  # Speed of speech
    engine.setProperty("volume", 1.0)  # Maximum volume

    # Find and set a female voice
    voices = engine.getProperty("voices")  # Get all available voices
    for voice in voices:
        if "female" in voice.name.lower() or "f" in voice.id.lower():
            engine.setProperty("voice", voice.id)
            break

    # Temporary filename to store the audio
    filename = "output_audio.mp3"

    # Save the audio to a file
    engine.save_to_file(text, filename)

    # Run the engine to process the file
    engine.runAndWait()

    return filename

# Gradio interface setup
iface = gr.Interface(
    fn=text_to_audio_pyttsx3,  # Function to be called
    inputs="text",  # Text input
    outputs="audio",  # Audio output
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch(share=True)
