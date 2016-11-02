
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route("/job", methods=["POST"])
def create_job():   
    try:
        contents = request.json # contents = GET JSON  
        print(contents["id"])
        dic = {'id':'nam'}
        list = [
            {'param':'f','val':2},
            {'param':'b','val':10}
            ]
    except KeyError as e:
        print("Json  error")
        
    return jsonify(results=dic)

if __name__ == "__main__":
   app.run()
