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

@app.route('/sendvideo', methods=['POST', 'GET'])
def sendvideo():
    """
    Receives a base64 encoded image as the img parameter and updates the global variable.
    Calls Rohan's function
    """
    if request.method=='POST':
        img = request.get_json(force=True)['img']
        
        img = base64.b64decode(img)
        buf = io.BytesIO(img)
        img = Image.open(buf)
        
        globalVar["image"] = img

        #Rohan's function???
        #for now, save to disk as test
        
        #img = img.save("downloaded.png")
        try:
            input_image = img.convert('RGB')
            #return(str(put_depths_in_dict(input_image)))
            r = put_depths_in_dict(input_image)
            return " ".join([str(r[0]), str(r[1][0]), str(r[1][1])])
        except Exception as e:
            return str(e)
    else:
        return 'HELLO WORLD'

def streamAudio():
    yield globalVar["audio"]

@app.route('/getaudio')
def getaudio():
    return 'Hello World'

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)
