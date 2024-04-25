from flask import Flask, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv('LIGHTUSERNAME')
ip_address = os.getenv('IP_ADDRESS')


app = Flask(__name__)

@app.route('/on', methods=['POST'])
def trigger_on():
    url = f"http://{ip_address}/api/{username}/lights/1/state"
    data = {"on" : True}

    request = requests.put(url, json=data)

    return jsonify({"received": True}), 200

@app.route('/off', methods=['POST'])
def trigger_off():
    url = f"http://{ip_address}/api/{username}/lights/1/state"
    data = {"on" : False}

    request = requests.put(url, json=data)

    return jsonify({"received": True}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081) 