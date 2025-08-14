from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import asyncio
from threading import Thread
from drone_telemetry_reading import run, set_socketio

app = Flask(__name__)
socketio = SocketIO(app)

# Pass the SocketIO instance to the drone script
set_socketio(socketio)

drone_thread = None

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("start_drone")
def start_drone():
    global drone_thread
    if drone_thread and drone_thread.is_alive():
        emit("log", {"message": "Drone process is already running!"})
        return

    emit("log", {"message": "Starting drone process..."})

    def start_drone_task():
        asyncio.run(run())  # Run the async drone `run` method

    drone_thread = Thread(target=start_drone_task)
    drone_thread.start()

@socketio.on("stop_drone")
def stop_drone():
    emit("log", {"message": "Stopping drone process is not yet implemented!"})

if __name__ == "__main__":
    socketio.run(app, debug=True)
