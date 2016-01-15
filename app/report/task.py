from threading import Thread
import subprocess
from app import socketio


def start_command_task(command):
    thread = Thread(target=execute_command, args=[command])
    thread.daemon = True
    thread.start()

def execute_command(command):
    print 'Running: %s' % command
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
    except OSError:
        print 'OSErrer'
    else:
        while True:
            line = p.stdout.readline()
            if not line:
                break
            print line
            emit_message(line)

def emit_message(message):
    socketio.emit('my response',{'data': message},namespace='/test')