from flask import Flask, request, send_from_directory
import pandas as pd
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests as http_requests
import os, uuid


"""
Next Steps:
    - Set up public URL (ngrok?)
    - Set up Twilio (which phone number to send stuff too)

    - Understand what is waiting for a request, what device it is on
    - Understand how requests are sent
    - Write chart generating code
    - Write analysis code
"""



API_KEY = "SK9323e0874c4c85dcac9ec83a4f71bafc"
API_SECRET = "AL6wvpjvV6i5V6sKv0f7k8eKaZNkWOI3"

Pending_Files = {}

#setup
Upload_Dir = "Uploads"
os.makedirs(Upload_Dir, exists_ok=True)
Graph_Dir = "Graphs"
os.makedirs(Graph_Dir, exist_ok=True)

#functions
def is_valid_name(name):
    """Return True if the name has at least one alphanumeric character and
    is short enough to be a reasonable file name."""
    return bool(name) and len(name) <= 50 and any(c.isalnum() for c in name)

def sanitize(name):
    return name.strip().replace(" ", "_").replace("/","").replace("\\", "")

def downloadFile(media_URL):
    r = http_requests.get(media_URL, auth=(API_KEY, API_SECRET), timeout=15)
    r.raise_for_status()
    return r.text


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])

def webhook():
    #Get data about incoming request
    sender = request.form.get("From");
    Num_Media = int(request.form.get("NumMedia", 0))
    body = request.form.get("Body", "").strip()
    resp = MessagingResponse()

    """----------------------------------if its expecting a name-----------------------------------------------"""
    if sender in Pending_Files:
    #Bad Name
        if Num_Media > 0:
            resp.message("Send which kind of meat you last cooked please!")
            return str(resp)
        if not body:
            resp.message("Thats an empty message dumbass")
            return str(resp)
        if not is_valid_name(body):
            resp.message("That isn't a valid name")
            return str(resp)
        
        #Successful Name | Renames file and saves to Upload_Dir
        temp_path = Pending_Files.pop(0)
        final_Name = sanitize(body)
        final_Path = os.path.join(Upload_Dir, f"{final_Name}.csv")
        os.rename(temp_path, final_Path)

        #Verify the file was renamed correctly
        if not os.path.exists(final_Path):
            resp.message("The File failed to rename. Final_Path DNE")
            return resp
        if os.path.getsize(final_Path) == 0:
            resp.message("The file was renamed, but there is no data in the file")
            return resp
        try:
            df = pd.read_csv(final_Path, header=10,skipinitialspace=True)
            if df.empty:
                resp.message("The file is saved, but has no data in it. Empty spreadsheet")
                return resp
        except Exception as e:
            resp.message(f"The file was saved, but couldn't be read as a .CSV: {e}")
            return resp
        
        #if it passes all the checks, it clears the pending list
        Pending_Files.clear()

    """-----------------------------------------Analysis Code-------------------------------------------------"""
    
    #Add Analysis Code HERE********* Plus .png and sms code
    
    """-----------------------------If not expecting a name, expecting file---------------------------------"""

    #Request File Info
    file_URL = request.form.get("MediaUrl0")
    file_type = request.form.get("MediaContentType0", "")

    allowed_types = ("text/plain", "text/csv", "application/csv", "application/octet-stream")

    if not any(t in file_type for t in allowed_types):
        resp.message(f"Please send a .csv or .txt file (got: {file_type}).")
        return str(resp)

    #Try putting URL content into file
    try: 
        Content = downloadFile(file_URL)
        
        #Inital Unique Name
        init_filename = f"{uuid.uuid4().hex}.csv"

        #adds filename to csv_path. Same as adding to folder
        csv_path = os.path.join(Upload_Dir, init_filename)
        with open(csv_path, "w") as f:
            f.write(Content)
    except Exception as e:
        resp.message(f"Could not download File: {e}")
        return resp
    
    #Add to pending for next round of requests
    Pending_Files[2] = {csv_path, sender}
    resp.message("Got your File! Now gimme a name")
    return resp
