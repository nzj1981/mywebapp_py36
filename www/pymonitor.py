# encoding: utf-8
""" 
@version: v1.0 
@author: autumner 
@license: Apache Licence  
@contact: 18322313385@163.com 
@site: https://github.com/nzj1981/mywebapp_py36.git 
@software: PyCharm 
@file: pymonitor.py 
@time: 2018/5/14 10:56
"""

__author__ = 'autumner'


'''
开启DEBUG模式,在开发模式自动重载程序
'''


import os, sys, time, subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def log(s):
    print('[Monitor] %s' % s)


class MyFileSystemEventHander(FileSystemEventHandler):

    def __init__(self, fn):
        super(MyFileSystemEventHander, self).__init__()
        self.restart = fn

    def on_any_event(self, event):
        if event.src_path.endswith('.py'):
            log('Python source file changed: %s' % event.src_path)
            self.restart()


command = ['echo', 'ok']
process = None


def kill_process():
    global process

    if process:
        log('Kill process [%s]...' % process.id)
        process.kill()
        process.wait()
        log('Process ended with code %s.' % process.returncode)
        process = None


def start_process():
    global process, command
    log('Start process %s...' % ' '.join(command))
    process = subprocess.Popen(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)


def restart_process():
    kill_process()
    start_process()


def start_watch(path, callback):
    observer = Observer()
    observer.schedule(MyFileSystemEventHander(restart_process), path, recursive=True)
    observer.start()
    log('Watch directory %s...' % path)
    start_process()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    argv = sys.argv[1:]

    if not argv:
        print('Usage: ./pymonitor your-script.py')
        exit(0)

    if argv[0] != 'python3':
        argv.insert(0, 'python3')

    command = argv
    path = os.path.abspath('.')
    start_watch(path, None)
