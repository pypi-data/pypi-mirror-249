from flask import Flask ,render_template
from flask_socketio import SocketIO, emit

from superide.home.rpc.handlers.app import AppRPC
from superide.home.rpc.handlers.os import OSRPC
from superide.home.rpc.handlers.project import ProjectRPC
from superide.boards.cli import _get_boards

# 创建一个 Flask 应用
# app = Flask(__name__)
# app.static_folder = './static/assets'
# app.template_folder='./static'
app = Flask(__name__, static_folder='static/assets', template_folder='static')
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')
    
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
   
@socketio.on("load_state")
def handle_load_state():
    emit("load_state", AppRPC.load_state())

@socketio.on("save_state")
def handle_save_state(data):
    emit("save_state", AppRPC.save_state(data))

@socketio.on("init")
def handle_init(data):
    board = data[0]
    framework = data[1]
    project_dir = data[2]
    emit("init",ProjectRPC.init(board, framework, project_dir))

@socketio.on("get_projects")
def handle_get_projects():
    emit("get_projects", ProjectRPC.get_projects())

@socketio.on("reveal_file")
def handle_reveal_file(data):
    emit("reveal_file", OSRPC.reveal_file(data))

@socketio.on("open_file")
def handle_open_file(data):
    emit("open_file", OSRPC.open_file(data))

@socketio.on("is_file")
def handle_is_file(data):
    emit("is_file", OSRPC.is_file(data))

@socketio.on("boards_json")
def handle_boards_json():
    emit("boards_json",_get_boards())
   
def run_server(host, port, no_open, shutdown_timeout, home_url):
    socketio.run(app, host="0.0.0.0")

if __name__ == '__main__':
    socketio.run(debug=True)