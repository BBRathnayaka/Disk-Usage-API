# Developed by Budditha Rathnayake

from flask import Flask, jsonify, request
import redis
from rq import Queue
import time
import os
import subprocess
import requests

app = Flask(__name__)

r = redis.Redis()

q=Queue(connection=r)

def dusage(n):
   delay = 2
   print("-------------------------------------")
   print("Task running")
   print('File name :',n)
   time.sleep(delay)
   out = os.popen('du -hs ' + n).read()
   print (out)

   usage = {'usage':out}
   x = requests.post('http://localhost:5000/result', json = usage)
   print (x)
   print(x.text)


@app.route('/', methods=['GET','POST'])
def index():
   if(request.method == 'POST'):
       data = request.get_json()

       name = data['name']
       location = data['location']

       job = q.enqueue(dusage, data['location'])

       return jsonify ({'result':'Success !','location': location}),201
   else:
       return jsonify({"result":"Fail","method":"get"})

@app.route('/result', methods=['POST'])
def result():
   req_data = request.get_json()
   print(req_data)
   return jsonify (req_data),200



if __name__ == '__main__':
   app.run(debug=True)


   # return os.system('du -hs ' + n)

   #sendResponse(usage, callback_url)

# def sendResponse(usage)
#     data = {
#         "size" : out
#     }
#     response = requests.post(data, callback_url)
#     print (response.text)

# @app.route('/usage',methods=['GET','POST'])
# def usage():
#     requests.post(data, callback_url)
#     res = requests.post(data['callback_uri'], json={"mytext":out})
#     if res.ok:
#         print (res.json())