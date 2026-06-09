from flask import Flask, request

app = Flask(__name__)

@app.route("/hello", methods=["GET"])
def hello():
    return "Hello world!"

app.run(port=5000)