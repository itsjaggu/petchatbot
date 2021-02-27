from flask import Flask, render_template, redirect, url_for
import chatgui

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/chat-bot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat-bot/call-chat-bot')
def botgui():
    chatgui.main()
    return redirect("/chat-bot", code=302)

if __name__ == "__main__":
    app.run(debug=True)