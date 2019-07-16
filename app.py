#!/usr/bin/python
import os
from ibm_watson import SpeechToTextV1
from flask import Flask, redirect, url_for, request, render_template
import json
from os.path import join, dirname
from werkzeug import secure_filename


app = Flask(__name__)

speech_to_text = SpeechToTextV1(
    iam_apikey='qIVfuJ6JLnojrM4KMZFHSfPbIKDIc_w3Dz43cL4ovYfU',
    url='https://stream.watsonplatform.net/speech-to-text/api'
)

def json2srt(j):
    jsondict = j
    result=jsondict["results"]
    srt=""
    count=0
    for sentence in result:
        altervative=sentence["alternatives"][0]
        transcript=altervative["transcript"]
        timestamp=altervative["timestamps"]
        begin_time=timestamp[0][1]
        end_time=timestamp[len(timestamp)-1][2]
        begin_h=int(begin_time // 3600)
        bh="{:0>2d}".format(begin_h)
        begin_m=int((begin_time - 3600*begin_h) // 60)
        bm="{:0>2d}".format(begin_m)
        begin_s=int(begin_time - 3600*begin_h - 60*begin_m)
        bs="{:0>2d}".format(begin_s)
        begin_ms=begin_time - int(begin_time)
        bms="{:.3f}".format(begin_ms)[2:]
        end_h=int(end_time // 3600)
        eh="{:0>2d}".format(end_h)
        end_m=int((end_time - 3600*end_h) // 60)
        em="{:0>2d}".format(end_m)
        end_s=int(end_time - 3600*end_h - 60*end_m)
        es="{:0>2d}".format(end_s)
        end_ms=end_time - int(end_time)
        ems="{:.3f}".format(end_ms)[2:]
        time=bh+':'+bm+':'+bs+','+bms+' --> '+eh+':'+em+':'+es+','+ems+'\n'
        srt=srt+str(count)+'\n'+time+transcript+'\n\n'
        count=count+1
    return srt




@app.route('/')
def home():
    return redirect(url_for('static', filename='pi.html'))

#handling the form data (upload) form pi.html
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
    #once the file is uploaded, it is sent to the speech to text service by calling the API
    with open(join(dirname(__file__),f.filename)) as audio_file:
      speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/mp3',
        timestamps=True
      ).get_result()


    #s=json.dumps(speech_recognition_results)
    text=json2srt(speech_recognition_results)

   
    #htmltext = '<p>'+str(s)+'</p></br>'
    htmltext = '<p>'+text+'</p></br>'
    
 
   
    return htmltext


 
      

if __name__ == '__main__':
  #server port is 8080
   port = int(os.getenv('PORT', 8080))
   app.run(host='0.0.0.0', port=port, debug=False)