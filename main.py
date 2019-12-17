import cv2
from flask import Flask, render_template, Response,request,redirect,url_for,jsonify
from camera import VideoCamera
import time
import datetime
import os
import shutil

import base64
import io
import face_recognition
import csv
from flask_cors import CORS
app = Flask(__name__, static_url_path = "/static/", static_folder = "static")
CORS(app)

@app.route('/')
def index():
    return render_template('index.html',videonable="yes")

def createemp(id,name,loc,bu):
    with open('static/data/Emp_details.csv','a') as csvfile:
        newemp=id+","+name+","+loc+","+bu
        csvfile.write(newemp+"\n")

def reademp(id):
    with open('Emp_details.csv') as csvfile:
       readCSV = csv.reader(csvfile, delimiter=',')
       for row in readCSV:
        if row[0]==ID:
            Name=row[1]
            Location=row[2]
            BU=row[3]

        
def recognizeface(imgname):
    
  images = os.listdir('Images')
  image_to_be_matched = face_recognition.load_image_file("static/Training/"+imgname)
  #image_to_be_matched =face_recognition.load_image_file(imgname)

  image_to_be_matched_encoded = face_recognition.face_encodings(
      image_to_be_matched)[0]

  recresult="Not Detected"
  for image in images:

      current_image = face_recognition.load_image_file("Images/" + image)

      current_image_encoded = face_recognition.face_encodings(current_image)[0]

      result = face_recognition.compare_faces(
          [image_to_be_matched_encoded], current_image_encoded)
      if result[0] == True:
        recresult=image 
  return recresult
def vcapture(camera,imgname):
    frame = camera.get_image()
    if os.path.exists("static/Training"):
        shutil.rmtree("static/Training")
    os.mkdir("static/Training")
    file = "static/Training/"+imgname
    cv2.imwrite(file, frame)
    camera.delete()
@app.route('/video_feed')
def video_feed():
   return render_template('index.html',videonable="yes")
@app.route('/correct',methods=['GET', 'POST'])
def correct():
    ID = request.form['id']
    with open('static/data/Attendance.csv') as csvfile:
       readCSV = csv.reader(csvfile, delimiter=',')
       alm=False
       resulthtml="<alert>"
       for row in readCSV:
           if len(row)>0:
               if row[0]==ID:
                   alm=True      
       if alm==False:
           with open('static/data/Attendance.csv','a') as csvfile:
               t=time.localtime()
               d= datetime.date.today()
               ctime=time.strftime("%H:%M:%S",t)
               newemp=ID+","+str(d)+","+str(ctime)
               csvfile.write(newemp+"\n")
    return render_template('saveimage.html') 



@app.route('/result',methods=['GET', 'POST'])
def result():
    t=time.localtime()
    d= datetime.date.today()
    ctime=time.strftime("%H_%M_%S",t)
    imgname=str(d)+"-"+str(ctime)+".jpg"
    # vcapture(VideoCamera(),imgname)
    data=request.form['file']
    encoded_data=data.split(',')[1].encode()
    if os.path.exists("static/Training"):
        shutil.rmtree("static/Training")
    os.mkdir("static/Training")
    file = "static/Training/"+imgname
    with open(file,"wb") as fh:
        fh.write(base64.decodebytes(encoded_data))
    recognized ="No face found"
    
    try:
        recognized=recognizeface(imgname)
        if recognized != "Not Detected":
            resulthtml="nodata,Match found with "+recognized+" but No details Found"
            ID=recognized
            with open('static/data/Emp_details.csv') as csvfile:
               readCSV = csv.reader(csvfile, delimiter=',')
               for row in readCSV:
                  if row[0]+".jpg"==ID:
                    if row[1] !="":  
                        resulthtml="found,"+row[0]+",<h2 id='matchtext'>Match Found!</h2><table id='emp'><tr><td><b>ID</b></td><td>"+row[0]+"</td></tr><tr><td><b>Name</b></td><td>"+row[1]+"</td></tr><tr><td><b>Location</b></td><td>"+row[2]+"</td></tr><tr><td><b>BU</b></td><td>"+row[3]+"</td></tr></table>"
            #return render_template('index.html',recresult=recognized,videonable="no",imgname=imgname)  
            return Response(resulthtml)
            
        else:
            resulthtml="notfound,"+imgname
            return Response(resulthtml)
            #return render_template('saveimage.html',imgn=imgname)      
    except:
        recognized ="<h3 style='color::#3498DB;'>Inproper face i.e blur/lowlight etc..<h3>" 
        resulthtml="notproper,"+recognized
        #return render_template('index.html',recresult=recognized,videonable="no",imgname=imgname)
        return Response(resulthtml)

    #return render_template('saveimage.html',imgn=imgname)
    resulthtml="notfount,"+imgname
    return Response(resulthtml)
  
   
@app.route('/saveimage/<imgname>',methods=['GET', 'POST'])
def saveimage(imgname):
    print("entered:"+request.method)
    if request.method == 'POST':
         srcfile="static\\Training\\"+imgname
         eid = request.form['eid']
         ename = request.form['ename']
         eloc = request.form['eloc']
         ebu = request.form['ebu']
         destfile="static\\Training\\"+eid+".jpg"
         os.rename(srcfile,destfile) 
         shutil.move(destfile, "Images\\")
         createemp(eid,ename,eloc,ebu)   
         return render_template('index.html')
    else:
         return render_template('saveimage.html',imgn=imgname)  

if __name__ == '__main__':
    app.config['SERVER_NAME'] = "localhost:5000"
    app.run(host='0.0.0.0', debug=True)
