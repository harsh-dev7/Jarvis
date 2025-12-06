import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! How can I help you?")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! How can I help you?")
    else:
        speak("Good Evening! How can I help you?")  
    speak("I am Jarvis. Please tell me how may I assist you.")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:    
        print("Sorry, I did not understand that. Please repeat.")
        speak("Sorry, I did not understand that. Please repeat.")
        return "None"
    except sr.RequestError:
        print("Sorry, I'm having trouble connecting to the internet.")
        speak("Sorry, I'm having trouble connecting to the internet.")
        return "None"
    return query


if __name__ == "__main__":
    wishMe() 
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = takeCommand().lower()
            if query != "None":
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                    print(results)
                except wikipedia.exceptions.DisambiguationError as e:
                    speak("There were multiple results. Can you be more specific?")
                    print(e)
                except wikipedia.exceptions.HTTPTimeoutError:
                    speak("The Wikipedia server timed out. Please try again later.")
                except Exception as e:
                    speak("An error occurred while searching Wikipedia.")
                    print(e)

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak("Opening Google...")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            speak("Opening Stack Overflow...")
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2' 
            try:
                songs = os.listdir(music_dir)
                if songs:
                    print(songs)    
                    os.startfile(os.path.join(music_dir, songs[0]))  
                    speak(f"Playing {songs[0]}")
                else:
                    speak("No songs found in the directory.")
            except FileNotFoundError:
                speak("Music directory not found. Please check the path.")
                print("Error: Music directory not found.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\user\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe" 
            if os.path.exists(codePath):
                os.startfile(codePath)
                speak("Opening Visual Studio Code...")
            else:
                speak("Visual Studio Code is not installed or the path is incorrect.")
                print("Error: VS Code path not found.")
                
        elif 'stop' in query or 'exit' in query:
            speak("Goodbye! Have a nice day.")
            break