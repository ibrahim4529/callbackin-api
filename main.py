import json
from pydoc import cli
from flask import Flask, jsonify, request
from paho.mqtt import client as mqtt_client

app = Flask(__name__)

@app.route("/<path>", methods=["GET", "POST"])
def callback(path):
    if request.is_json:
        body = request.get_json()
    else:
        body = "none data json"
    headers = dict(request.headers)
    client = mqtt_client.Client()
    client.connect("mqtt.eclipseprojects.io")
    payload = json.dumps({
        "body": body,
        "headers": headers,
    })
    client.publish(topic=path, payload=payload)
    client.disconnect()
    return "success"


