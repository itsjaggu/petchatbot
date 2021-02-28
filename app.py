# Flask app to load the chat bot on an html page
from flask import Flask, render_template
from flask_socketio import SocketIO
import chatgui

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

# base route for landing page
@app.route("/")
def sessions():
    return render_template('chatbot.html')

# function to callout successful receive of message
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

# This route loads the windows based GUI for chatbot, however disabled for final deployment as Heroku doesn't support tkinter package
""" @app.route('/chat-bot')
def botgui():
    chatgui.main()
    return redirect("/chat-bot", code=302) """

# this is primary even handler and connector between html java script and Flask app
@socketio.on('my event')
def handle_my_custom_event(msg, methods=['GET', 'POST']):
    # print msg from the user
    print('received my event: ' + str(msg))
    socketio.emit('my response', msg, callback=messageReceived)
    
    # passing user message to chatbot to get response from trained model
    msg_str = msg["message"]
    res = chatgui.chatbot_response(msg_str)
    res_json = {'user_name': 'BOT', 'message': res}
    
    # displaying results from taring model to the user
    socketio.emit('my response', res_json, callback=messageReceived)

if __name__ == "__main__":
    #app.run(debug=True)
    socketio.run(app, debug=False)