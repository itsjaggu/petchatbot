from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO
import json
import chatgui

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route("/")
def sessions():
    return render_template('chatbot.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

""" @app.route('/chat-bot')
def botgui():
    chatgui.main()
    return redirect("/chat-bot", code=302) """

@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    print('received my event: ' + str(msg))
    socketio.emit('my response', msg, callback=messageReceived)
    
    msg_str = msg["message"]
    res = chatgui.chatbot_response(msg_str)
    res_json = {'user_name': 'BOT', 'message': res}
    
    socketio.emit('my response', res_json, callback=messageReceived)

if __name__ == "__main__":
    #app.run(debug=True)
    socketio.run(app, debug=True)