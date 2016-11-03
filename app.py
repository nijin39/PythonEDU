# -*- coding: utf-8 -*-

from flask import Flask
from flask import jsonify
from flask import request
import json
import subprocess
import time
import requests

app = Flask(__name__)
app.config.from_pyfile('config.properties')

PATH = app.config["PATH"]
URL = app.config["URL"]

success_message = {'status':'success','message':'received'}
failed_message = {'status':'failed','message':'received'}

    
'''
    cmd command run
'''
def subprocess_open(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

'''
1. Request Body Parsing
2. Validate Content
3. Send Response
'''


def SaveFileAndRun(dict):
    
    
    yesBatch = {'Status':'Success','Message':'Create File'}
    noBatch = {'Status':'Fail','Message':'Creation Error Occured'}
    
    ex_dic1 = {'Status':'Success','Message':'dir','Type':'bat'}
    ex_dic2 = {'Status':'Success','Message':'dir','Type':'pirlo'}
    
    '''
                클라이언트로부터 받은 dictionary를 파라미터로 받음.  
                딕셔너리의 Type값이 bat일 경우 매세지의 내용을 저장하고 성공 메세지를 반환
                딕셔너리의 Type값이 bat이 아닐 경우 별도의 과정 없이 실패 메세지를 반환
    '''
    
    
    fileName = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    
    if (dict["type"]=='bat'):
        try :  
            savefilePointer = open(PATH + fileName + '.bat','w')
            
            fileContent = dict["script"]
            savefilePointer.write(fileContent)
            
            response = requests.request("PUT", URL + fileName, data=json.dumps(yesBatch), verify=False)
             
        except IOError as e:
            print("I/O error : " + str(e))
    
        except:
            print ("Error Occured")
            
        finally:
            savefilePointer.close()
            
        #.bat 실행 
        if response.text == "GOOD":
            print(subprocess_open(PATH + fileName + '.bat')[0])
            
        else:
            print ("Connection Error")  
            
    else:
         response = requests.request("PUT", URL + fileName, data=json.dumps(noBatch), verify=False)
             
             

@app.route("/job", methods=["POST"])
def create_job():
    try:
        # 1. Request Body Parsing
        contents = request.json
        id = contents["id"]
        script = contents["script"]
        type = contents["type"]

    except KeyError as e:
        print("Key error")
        return json.dumps(failed_message)

    else:    
        '''
        2. Validate Content
        must be id / script /type 
        id     : integer
        script : 5000 byte
        type   : batch / bash / ksh / csh / python
        '''
        if(id and script and type):
            # 3. Send Response
            
            response = requests.request("PUT", URL+id, data=json.dumps(success_message), verify=False)
            SaveFileAndRun(contents)
            return jsonify(results=success_message)
        else:
            response = requests.request("PUT", URL+id, data=json.dumps(failed_message), verify=False)


    
if __name__ == "__main__":
   app.run()
    
