from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

@app.route("/")
def hello():
    return "HEELO WORLD!!!!"

@app.route("/restful")
def restTest():
    dic = {'name':'yongnamdo', 'script':'script', 'bitrh': '1118'}
    return jsonify(results=dic)

@app.route("/json")
def index():
    list = [
        {'param':'f','val':2},
        {'param':'b','val':10}
        ]
    return jsonify(result=list)

@app.route("/job", methods=["POST"])


def create_job():
    print("enter create job")
    
    try:
        contents = request.json # contents 
        print(contents["idid"])
        list = [
            {'param':'f','val':2},
            {'param':'b','val':10}
            ]
    except KeyError as e:
        print("Json  error")
        
    return jsonify(result=list)


if __name__ == "__main__":
   app.run()