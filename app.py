# -*- coding: utf-8 -*-
# -*- coding: ms949 -*-
import os
import json
import time
import psutil
import requests
import subprocess

from flask import Flask
from flask import jsonify
from flask import request
from psutil import disk_partitions

app = Flask(__name__)
app.config.from_pyfile('config.properties')

PATH = app.config["PATH"]
URL = app.config["URL"]
POSTURL = app.config["POSTURL"]

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
    shell command run
'''
def cmdprocess_open(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    (stdoutdata, stderrdata) = popen.communicate()
    return stdoutdata, stderrdata

'''
            
1. Request Body Parsing
2. Validate Content
3. Send Response
4. received dictionary from client 
5. Validate Value type
6. execute bat 
7. Send post result    
'''

''' execute batch file'''
def SaveFileAndRun(dict):
    
    yesBatch = {'Status':'Success','Message':'Create File'}
    noBatch = {'Status':'Fail','Message':'Creation Error Occured'}
    
    fileName = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    '''file name is 'YearMonthDay_HoursMinuteSeconds'.'''
    
    #5. Validate Value type
    if (dict["type"]=='bat'):
        try :  
            savefilePointer = open(PATH + fileName + '.bat','w')
            
            fileContent = dict["script"]
            savefilePointer.write(fileContent)
            
            #response = requests.request("PUT", URL + fileName, data=json.dumps(yesBatch), verify=False)
             
        except IOError as e:
            print("I/O error : " + str(e))
    
        except:
            print ("Error Occured")
            
        finally:
            savefilePointer.close()
            
        #6. execute bat  
        if True:#response.text == "GOOD":
            post_result = {}
            pcs_result = subprocess_open(PATH + fileName + '.bat')
            
             #7. Send post result   
            if len(pcs_result[1]) == 0:
                post_result['status'] = "success_excute"
                post_result['message'] = pcs_result[0]
            else:
                post_result['status'] = "failed_excute"
                post_result['message'] = pcs_result[1]    
        else:
            print ("Connection Error")   
        
        #response = requests.request("POST", POSTURL, data=json.dumps(post_result, ensure_ascii=False), verify=False)
        cmdprocess_open('del ' +  PATH + fileName + '.bat')
        return post_result['message']

    else:
         response = requests.request("PUT", URL + fileName, data=json.dumps(noBatch), verify=False)
         return noBatch["Status"]
             
             

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
            #response = requests.request("PUT", URL+id, data=json.dumps(success_message), verify=False)
            
            # 4.received dictionary from client 
            return_value=SaveFileAndRun(contents)
            return return_value
            
        else:
            response = requests.request("PUT", URL+id, data=json.dumps(failed_message), verify=False)
            return jsonify(results=failed_message)
        
        
'''
    get server CPU process info
'''
@app.route("/system/cpus", methods=["POST"])
def get_pcsinfo():

    cpu_idx = 0
    cmd_result = {}
    cmd_result['CpuNum'] = ""  
    cmd_result['Usage'] = ""
    cmd_cpu = psutil.cpu_percent(interval=1, percpu=True)
    
    for cpu_pcnt in cmd_cpu:
         cpu_idx += 1 
         cmd_result['CpuNum'] = cpu_idx
         cmd_result['Usage'] = cpu_pcnt
         print (str(cpu_idx) + " : " + str(cpu_pcnt) + "%") 
         #response = requests.request("POST", CPUURL, data=json.dumps(cmd_result), verify=False)
                    
    return str(cpu_idx)

'''
    get server DISKS process info
'''
@app.route("/system/disks", methods=["POST"])
def get_diskinfo():
    disk_list=[]
    disk_dictionary = {'mountpoint':''}
    disk_dictionary['usage']=''

    for disk in disk_partitions():
        mountpoint_value = disk.mountpoint  
          
        if disk.fstype == "NTFS":
            usage_value = str(psutil.disk_usage(disk.mountpoint).percent)       
            disk_dictionary['mountpoint'] = mountpoint_value
            disk_dictionary['usage'] = usage_value
            disk_list.append(disk_dictionary.copy())
            print ("dict : " + str(disk_dictionary))
            print (disk_list)
        else:
            continue
    return jsonify(results=disk_list)
    
if __name__ == "__main__":
   app.run()