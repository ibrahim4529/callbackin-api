import json
from flask import Flask, request
from paho.mqtt import client as mqtt_client

app = Flask(__name__)


@app.get("/")
def index():
    return {
        "name": "Callbackin API",
        "version": "0.0.1",
        "description": "A simple app for provide simple callback from public to localhost over mqtt",
        "endpoints": [
            {
                "name": "endpoint for callback",
                "path": "/{path}",
                "method": "GET/POST",
                "description": "This endpoint is for receive data from provider and send to localhost over mqtt",
            }
        ]
    }


@app.route("/<path>", methods=["GET", "POST"])
def callback(path):
    """
    Callback endpoint for receive data from provider and send to localhost over mqtt
    """
    if request.is_json:
        body = request.get_json()
    else:
        body = "none data json"
    headers = dict(request.headers)
    payload = json.dumps({
        "body": body,
        "headers": headers,
    })
    send_back_data_over_mqtt(path, payload)
    return {
        "message": "Sucess Calling Callback",
    }


def send_back_data_over_mqtt(path, payload):
    """
    Send data to localhost over mqtt
    topic is based on path and payload is json string
    """
    client = mqtt_client.Client()
    client.connect("mqtt.eclipseprojects.io")
    client.publish(topic=path, payload=payload)
    client.disconnect()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)