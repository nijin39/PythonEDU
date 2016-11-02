# -*- coding: utf-8 -*-

import subprocess
import time
import json
import requests

from flask import request
from flask import Flask
from flask import jsonify

app = Flask(__name__)
app.config.from_pyfile('config.properties')

yesBatch = {'Status':'Success','Message':'Create File'}
noBatch = {'Status':'Fail','Message':'Creation Error Occured'}

ex_dic1 = {'Status':'Success','Message':'dir','Type':'bat'}
ex_dic2 = {'Status':'Success','Message':'dir','Type':'pirlo'}


'''
    cmd 명령어 실행
'''
def subprocess_open(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

'''
     클라이언트로부터 받은 dictionary를 파라미터로 받음.  
    딕셔너리의 Type값이 bat일 경우 매세지의 내용을 저장하고 성공 메세지를 반환
    딕셔너리의 Type값이 bat이 아닐 경우 별도의 과정 없이 실패 메세지를 반환
'''
def cmdProcess(dict):
    PATH = app.config["PATH"]
    URL = app.config["URL"]
    fileName = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    
    if (dict.get('Type')=='bat'):
        try :  
            savefilePointer = open(PATH + fileName + '.bat','w')
            
            fileContent = dict.get('Message')
            savefilePointer.write(fileContent)
            
            response = requests.request("PUT", URL + fileName, data=json.dumps(yesBatch), verify=False)
             
        except IOError as e:
            print("I/O error : " + e)
    
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

if __name__ == "__main__":
    cmdProcess(ex_dic1)
    cmdProcess(ex_dic2)    

