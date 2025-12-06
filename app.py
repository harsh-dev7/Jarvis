from flask import Flask, request, jsonify
import wikipedia,os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Jarvis Online API is running!"})

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    command = data.get("command", "").lower()

    if "hello" in command:
        return jsonify({"reply": "Hello sir, how can I assist you?"})

    elif "who is" in command or "what is" in command:
        try:
            topic = command.replace("who is", "").replace("what is", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            return jsonify({"reply": summary})
        except:
            return jsonify({"reply": "Sorry sir, I could not find information on that topic."})

    elif "open youtube" in command:
        return jsonify({
            "reply": "Opening YouTube sir.",
            "action": "open_url",
            "url": "https://youtube.com"
        })

    elif "open google" in command:
        return jsonify({
            "reply": "Opening Google sir.",
            "action": "open_url",
            "url": "https://google.com"
        })

    return jsonify({"reply": "Sorry sir, I did not understand the command."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)