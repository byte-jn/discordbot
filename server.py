from flask import Flask
from threading import Thread
from datetime import datetime  # Import datetime

app = Flask(__name__)
start_time = datetime.utcnow()  # Define start_time here

@app.route("/")
def hello():
    elapsed_time = datetime.utcnow() - start_time
    elapsed = int(elapsed_time.total_seconds())
    a = f"Discord Bot (Poaoao) is running for {round(elapsed)} seconds"
    return a

def run():
    app.run(host="0.0.0.0")

def Live(start_time_param):  # Pass start_time as a parameter
    global start_time  # Use the global keyword to modify the global variable
    start_time = start_time_param
    t = Thread(target=run)
    t.start()
  