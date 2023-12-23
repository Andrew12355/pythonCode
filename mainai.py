import openai
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import datetime  # Add this line to import datetime module

openai.api_key = "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"
completion = openai.Completion()

MASTER = "Boss Andrew..."

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning" + MASTER)
    elif 12 <= hour < 18:
        speak("Good Afternoon" + MASTER)
    else:
        speak("Good Evening" + MASTER)

    speak("I am Super Ring, How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"Boss said: {query}\n")
        #check for pause command
        if 'pause' in query.lower():
            speak("Pausing...")  # Add a response to indicate the pause
            return "pause"
        
        return query

    except Exception as e:
        print(e)
        return None

def get_openai_response(query):
    prompt = f'Boss: {query}\n Bard: '
    response = completion.create(prompt=prompt, engine="text-davinci-002", stop=['\Chando'], max_tokens=200)
    answer = response.choices[0].text.strip()
    return answer

def main():
    wishMe()
    paused = False  # Initialize the variable outside the loop
    while True:
        query = takeCommand()

        if query:
            query = query.lower()
            if 'pause' in query:
                paused = not paused  # Toggle the pause state
                if paused:
                    speak("Assistant paused.")
                else:
                    speak("Resuming...")
            elif 'resume' in query:
                paused = False
                speak("Resuming...")
            elif not paused:
                if 'wikipedia' in query:
                    speak("Searching Wikipedia...")
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=2)
                    print(results)
                    speak(results)

                elif 'open youtube' in query:
                    webbrowser.open("https://www.youtube.com")

                elif 'open google' in query:
                    webbrowser.open("https://www.google.com")

                elif 'time' in query:
                    time_now = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"The current time is {time_now}")

                elif 'thanks' in query:
                    speak("Alright Boss... Have a great day!")
                    break

                elif 'hi' in query:
                    speak("Hi Boss, yosh daebak?")

                else:
                    openai_response = get_openai_response(query)
                    print("Answer:", openai_response)
                    speak(openai_response)

if __name__ == "__main__":
    main()
