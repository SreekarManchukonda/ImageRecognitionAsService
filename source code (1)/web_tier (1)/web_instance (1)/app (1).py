import os
import threading
import time
from flask import Flask, render_template, request
from flask import Response
import json
#from web_tier.uploader import UploadToS3

from uploader import push_image, pull_response

template_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(template_dir, 'web_app')
static_dir = os.path.join(template_dir, 'static')
template_dir = os.path.join(template_dir, 'templates')


app = Flask(__name__,template_folder=template_dir, static_folder=static_dir)

userPhotos = {} 

class userimages:
   userdict = {}
   def __init__(self):
      pass

@app.route('/', methods = ['POST', 'GET'])
def home():
   return render_template('index.html')

@app.route('/api/photo', methods = ['POST', 'GET'])
def upload():
   
   global userPhotos
   userPhotos = {}
   for index in range(len(request.files.getlist('userPhoto'))):
        
        image = request.files.getlist('userPhoto')[index]
        
        
        push_image.push_to_sqs(image)
        userPhotos[image.filename]=''
   return ""

@app.route('/upload', methods = ['POST', 'GET'])
def upload_from_generator():
   
   image = request.files.getlist('myfile')[0]
   filename = image.filename
   print(image.filename +'\n')
   push_image.push_sqs_from_generator(image)
   user_obj = userimages()
   user_obj.userdict[filename]=''
   time.sleep(25)
   result_obj = pull_response.pull_image_for_generator(user_obj,filename)
   print(result_obj.userdict[filename])
   print(result_obj.userdict)
   #result = '('+filename+','+ result_obj.userdict[filename] +')'
   
   return Response(str(result_obj.userdict[filename]))

@app.route('/receive', methods = ['POST', 'GET'])
def download():
   result_dict = pull_response.pull_from_sqs(userPhotos)
   print(result_dict)
   result_size = len(result_dict)

   return render_template('response.html',result_dict=result_dict,result_size=result_size)
if __name__ == '__main__':
   app.run(debug=False,use_reloader=False,threaded=True,host='0.0.0.0',port=5000)
