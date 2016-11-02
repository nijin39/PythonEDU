
from flask import Flask
from flask import jsonify
from flask import request
import json

app = Flask(__name__)

success_message = {'status':'success','message':'received'}
failed_message = {'status':'failed','message':'received'}

'''
1. Request Body Parsing
2. Validate Content
3. Send Response
'''
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
            return json.dumps(success_message)
        else:
            return json.dumps(failed_message)

if __name__ == "__main__":
   app.run()
