from threading import Thread
import subprocess
from app import socketio
import time
from app import app

def start_command_task(command):
    thread = Thread(target=execute_command, args=[command])
    thread.daemon = True
    thread.start()

def execute_command(command):
    app.logger.info('Running: %s' % command)
    overall_result = ''
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
    except OSError:
        print 'OSErrer'
    else:
        time.sleep(3)
        while True:
            line = p.stdout.readline()
            if not line:
                break
            overall_result += line + '\n'
            emit_message(line)
        app.logger.info(overall_result)
def emit_message(message):
    socketio.emit('my response',{'data': message},namespace='/test')