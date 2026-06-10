from flask import Flask, request, send_from_directory
import pandas as pd
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests as http_requests
import os, uuid
from dotenv import load_dotenv
import analysis as a


load_dotenv()

"""
Next Steps:
    - Set up public URL (ngrok?)
    - Set up Twilio (which phone number to send stuff too)

    - Understand what is waiting for a request, what device it is on
    - Understand how requests are sent
    - Write chart generating code
    - Write analysis code
"""




#setup file storage
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
Graph_Dir = os.path.join(BASE_DIR, "charts")
Upload_Dir = os.path.join(BASE_DIR, "uploads")
os.makedirs(Upload_Dir, exist_ok=True)
os.makedirs(Graph_Dir, exist_ok=True)

app = Flask(__name__)

@app.route("/")
def index():
    return '''
        <html>
            <body>
                <h2>ChefIQ Analyzer</h2>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <label>Name Your File:<label><br>
                    <input type="text" name="custom_name" placeholder="e.g. Brisket_10-6-26"><br><br>
                    <input type="file" name="file" accept=".csv,.txt">
                    <button type="submit">Analyze</button>
                </form>
            </body>
        </html>
    '''

@app.route("/upload", methods=["POST"])

def upload():
    if "file" not in request.files:
        return "No file idiot", 400
    file = request.files["file"]

    if file.filename == "":
        return "No File Selected, idiot", 400
    

    custom_name = request.form.get("custom_name", "").strip()
    if not custom_name or not any(c.isalnum() for c in custom_name):
        custom_name = file.filename
    
    file_name = custom_name.replace(" ", "_").replace("/", "").strip() + ".csv"
    file_path = os.path.join(Upload_Dir, file_name)
    file.save(file_path)

    fig = a.analyze(file_path)

    chart_name = f"{custom_name}_Chart.png"
    chart_path = os.path.join(Graph_Dir, chart_name)
    fig.savefig(chart_path, dpi=150, bbox_inches="tight")

    print("Saved chart to:", chart_path)
    print("File exists?", os.path.exists(chart_path))


    return f'''
        <html>
            <body>
                <h2>✅ File received: {file_name}</h2>
                <p>Your analysis is ready!</p>
                <img src="charts/{chart_name}" style="max-width:100%">
                <br><br>
                <a href="charts/{chart_name}" download="{chart_name}">
                    ⬇️ Download Chart
                </a>
                &nbsp;&nbsp;
                <a href="/Uploads/{file_name}" download="{file_name}">
                    ⬇️ Download Original File
                </a>
                <br><br>
                <a href="/">Upload another file</a>
            </body>
        </html>
    '''

@app.route("/charts/<filename>")
def serve_chart(filename):
    return send_from_directory(Graph_Dir, filename)

@app.route("/Uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(Upload_Dir, filename)


app.run(host="0.0.0.0", port=5001)