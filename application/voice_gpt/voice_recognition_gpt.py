from dotenv import load_dotenv
import os
import openai
import pyttsx3
import speech_recognition as sr

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Missing OpenAI API Key. Make sure it's set in the .env file.")

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=api_key)

# Initialize text-to-speech engine
engine = pyttsx3.init()

def text_to_speech(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
    """Convert speech to text using Google Speech Recognition."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            print("Processing...")
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
        except sr.RequestError as e:
            print(f"Could not request results: {e}")
        return ""

def chat_with_gpt(prompt):
    """Generate a response from OpenAI GPT-4."""
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def transcribe_audio(audio_file_path):
    """Transcribe an audio file to text."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        raise ValueError(f"Error in voice recognition: {e}")

def main():
    """Main function to interact with GPT-4 using voice."""
    print("Voice GPT Chat Started. Say 'exit' to quit.")
    while True:
        user_input = speech_to_text()
        if "exit" in user_input.lower():
            print("Goodbye!")
            break
        if user_input:
            print(f"You said: {user_input}")
            response = chat_with_gpt(user_input)
            print(f"GPT: {response}")
            text_to_speech(response)

if __name__ == "__main__":
    main()
