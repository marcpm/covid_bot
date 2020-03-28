from pathlib import Path
import requests
from config import PUSHOVER_CREDENTIALS

def push_to_ios(message, image_path):
    if image_path is not None:
        path = Path(image_path)
        suffix = path.suffix.lower().strip(".")
        if suffix.replace("e","")  in ["jpg","gif","png"]:
            extension = "jpeg" if suffix == "jpg" else suffix
        else:
            raise IOError ("File extension not accepted, request cancelled.")
        files =  {"attachment": (str(path.name), open(image_path, "rb"), "image/"+str(extension))}
    else:
        files = None
    response = requests.post("https://api.pushover.net/1/messages.json", data = {
      "token": PUSHOVER_CREDENTIALS["token"],
      "user": PUSHOVER_CREDENTIALS["user"],
      "message": message},files = files  )
    return response.text
