import openai
import pyttsx3
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = 'your_openai_api_key'

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def speech_to_text():
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
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
    
def transcribe_audio(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
        return text
    except Exception as e:
        raise ValueError(f"Error in voice recognition: {e}")

def main():
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

