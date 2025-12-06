from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import threading
import os

app = Flask(__name__)
CORS(app)

# -------- THREAD-SAFE TTS --------
def speak(text):
    def say():
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    threading.Thread(target=say).start()

# -------- GREETING --------
def get_greeting():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        return "Good Morning! How can I help you?"
    elif hour < 18:
        return "Good Afternoon! How can I help you?"
    else:
        return "Good Evening! How can I help you?"

# -------- COMMAND PROCESSOR --------
def process_command(query):
    query = query.lower()
    response = {"status": "success", "message": ""}

    if "wikipedia" in query:
        speak("Searching Wikipedia")
        topic = query.replace("wikipedia", "").strip()
        if topic == "":
            response["message"] = "Please say what to search on Wikipedia."
        else:
            info = wikipedia.summary(topic, sentences=2)
            response["message"] = info
            speak(info)

    elif "open youtube" in query:
        response["message"] = "Opening YouTube"
        speak(response["message"])
        threading.Thread(target=webbrowser.open, args=("https://youtube.com",)).start()

    elif "open google" in query:
        response["message"] = "Opening Google"
        speak(response["message"])
        threading.Thread(target=webbrowser.open, args=("https://google.com",)).start()

    elif "time" in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        response["message"] = f"Time is {time}"
        speak(response["message"])

    else:
        response["message"] = "I did not understand that."
        speak(response["message"])

    return response

# -------- ROUTES --------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/greeting")
def greeting():
    return jsonify({"greeting": get_greeting()})

@app.route("/api/command", methods=["POST"])
def command():
    query = request.json.get("query", "")
    return jsonify(process_command(query))

@app.route("/api/listen", methods=["POST"])
def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=10, phrase_time_limit=5)

        text = r.recognize_google(audio, language="en-in")
        return jsonify({"status": "success", "query": text})
    except sr.UnknownValueError:
        return jsonify({"status": "error", "message": "I didn't understand."}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)