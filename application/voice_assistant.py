import openai
import speech_recognition as sr
import pyttsx3

# Set up OpenAI API key
openai.api_key = "OPENAI_API_KEY"

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set up speech recognizer
recognizer = sr.Recognizer()

def speak(text):
    """Convert text to speech and speak it out loud."""
    engine.say(text)
    engine.runAndWait()

def get_gpt_response(user_input):
    """Send the user input to the OpenAI API and get the GPT response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can change to "gpt-4" if needed
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

def listen_to_user():
    """Listen to the user's speech and return the recognized text."""
    with sr.Microphone() as source:
        print("Say something to start the conversation, or 'quit' to exit.")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen for the user's speech

        try:
            # Recognize speech using Google's speech recognition
            user_input = recognizer.recognize_google(audio)
            print(f"You said: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print("Sorry, I'm having trouble with the speech service.")
            return None

def main():
    """Main function to run the voice assistant."""
    while True:
        user_input = listen_to_user()

        if user_input:
            if user_input.lower() == "quit":
                print("Goodbye!")
                speak("Goodbye!")
                break

            # Get GPT response based on user input
            gpt_response = get_gpt_response(user_input)
            print(f"Assistant: {gpt_response}")
            speak(gpt_response)
        else:
            # If no input or unrecognized input, continue listening
            continue

if __name__ == "__main__":
    main()
