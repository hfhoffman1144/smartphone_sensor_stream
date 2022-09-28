from datetime import datetime
from distutils.log import debug
import json
from collections import deque
from flask import Flask, request
import socket

hostname = socket.gethostname()
print(socket.gethostbyname(hostname))  

server = Flask(__name__)

MAX_DATA_POINTS = 1000
UPDATE_FREQ_MS = 100

time = deque(maxlen=MAX_DATA_POINTS)
accel_x = deque(maxlen=MAX_DATA_POINTS)
accel_y = deque(maxlen=MAX_DATA_POINTS)
accel_z = deque(maxlen=MAX_DATA_POINTS)

@server.route("/")
def index():
    ip_address = request.remote_addr
    return "Requester IP: " + ip_address


@server.route("/data", methods=["POST"])
def data():  # listens to the data streamed from the sensor logger
	if str(request.method) == "POST":
		print(f'received data: {request.data}')
		data = json.loads(request.data)
		print(data)
	return "success"


if __name__ == "__main__":
    server.run(debug=False, host="0.0.0.0")
     