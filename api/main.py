#main.py
from flask import Flask, request, Response
import base64
import io
from PIL import Image
import sys
sys.path.append("..")
from monodepth2.depth_estimator import put_depths_in_dict


app = Flask(__name__)

globalVar = {"image": None, "audio": None}

@app.route('/')
def home():
    return 'Hello World'

@app.route('/sendvideo')
def sendvideo():
    """
    Receives a base64 encoded image as the img parameter and updates the global variable.
    Calls Rohan's function
    """
    img = request.args['img']
    
    img = base64.b64decode(img)
    buf = io.BytesIO(img)
    img = Image.open(buf)
    
    globalVar["image"] = img

    #Rohan's function???
    #for now, save to disk as test
    
    #img = img.save("downloaded.png")
    try:
        input_image = img.convert('RGB')
        return(str(put_depths_in_dict(input_image)))
    except:
        return 'Hello World'

def streamAudio():
    yield globalVar["audio"]

@app.route('/getaudio')
def getaudio():
    return 'Hello World'

if __name__ == '__main__':
    app.run(threaded=True, processes=1)
