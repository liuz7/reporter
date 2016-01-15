from threading import Thread
import subprocess

def start_command_task(command):
    thr = Thread(target=execute_command(command))
    thr.start()

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