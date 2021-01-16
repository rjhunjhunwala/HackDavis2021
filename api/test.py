import requests
import base64
import io
from PIL import Image

URL = "http://127.0.0.1:5000/sendvideo"

with open("0001.jpg", "rb") as imgfile:
    msg = base64.b64encode(imgfile.read())
    param = {"img": msg}
    print(requests.get(url = URL, params = param).text)