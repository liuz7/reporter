from app import app
from app import socketio

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5050)
    socketio.run(app, host='0.0.0.0', port=5050)