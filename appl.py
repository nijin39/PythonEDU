# -*- coding: utf-8 -*-

import subprocess
import time
import json
import requests

from flask import request
from flask import Flask
from flask import jsonify

'''
def subpcs_open(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell=True)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

'''

# 배치 파일이 저장될 경로
PATH = "C:\\tempfiles\\"

# yesBatch : 파일 생성 성공시 반환하게 될 딕셔너리
# noBatch : 파일 생성 실패시 반환하게 될 딕셔너리
yesBatch = {'Status':'Success','Message':'Create File'}
noBatch = {'Status':'Fail','Message':'Creation Error Occured'}

ex_dic1 = {'Status':'Success','Message':'dir','Type':'bat'}
ex_dic2 = {'Status':'Success','Message':'dir','Type':'pirlo'}

app = Flask(__name__)

#딕셔너리의 Type값이 bat일 경우 매세지의 내용을 저장하고 성공 메세지를 반환
#딕셔너리의 Type값이 bat이 아닐 경우 별도의 과정 없이 실패 메세지를 반환

@app.route("/job")
def cmdProcess():
    
    if (ex_dic1.get('Type')=='bat'):
        try :           
            fileName = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            f = open(PATH + fileName + '.bat','w')
            fileContent = ex_dic1.get('Message')
            
            f.write(fileContent)
            f.close()
            
            #response = requests.request("PUT", 'http://127.0.0.1:5000', data=json.dumps(yesBatch), verify=False)
            return jsonify(results=yesBatch)
        
        except IOError as e:
            print("I/O error : " + e)
    
        except:
            print ("Error Occured")
    else:
        return jsonify(results=noBatch)



if __name__ == "__main__":
    app.run()
    

