import os
import sys
import threading
import time
import socket
from http.server import SimpleHTTPRequestHandler, HTTPServer
import webview

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def get_web_dir():
    if getattr(sys, 'frozen', False):
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass and os.path.exists(os.path.join(meipass, 'dist', 'index.html')):
            return os.path.join(meipass, 'dist')
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
        if os.path.exists(os.path.join(exe_dir, 'dist', 'index.html')):
            return os.path.join(exe_dir, 'dist')
        if os.path.exists(os.path.join(exe_dir, 'index.html')):
            return exe_dir
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(script_dir, 'dist')
    if os.path.exists(os.path.join(dist_dir, 'index.html')):
        return dist_dir
    return script_dir

class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        if directory is None:
            directory = get_web_dir()
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        pass

def start_server(port, root_dir):
    def handler_factory(*args, **kwargs):
        return QuietHTTPRequestHandler(*args, directory=root_dir, **kwargs)
    
    server_address = ('127.0.0.1', port)
    httpd = HTTPServer(server_address, handler_factory)
    httpd.serve_forever()

if __name__ == '__main__':
    web_dir = get_web_dir()
    port = find_free_port()
    
    server_thread = threading.Thread(target=start_server, args=(port, web_dir), daemon=True)
    server_thread.start()
    
    time.sleep(0.3)
    
    url = f"http://127.0.0.1:{port}/index.html"
    window = webview.create_window(
        title="MedPrep Pro - Global Medical Exam Prep Platform",
        url=url,
        width=1280,
        height=820,
        resizable=True,
        min_size=(900, 600)
    )
    webview.start()
