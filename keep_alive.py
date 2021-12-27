from flask import Flask
from threading import Thread
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def main():
  return "The bot is alive!"

def run():
  host, port = "0.0.0.0", 8080
  print(f"Serving on http://{host}:{port}")
  app.run(host=host, port=port)

def keep_alive():
  server = Thread(target=run)
  server.daemon = True
  server.start()
