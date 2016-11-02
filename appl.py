from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

@app.route("/restful")
def restTest():
    dic = {'name':'pey','phone':'01074888996','birth':'1026'}
    return jsonify(results=dic)

@app.route("/json")
def index():
    list = [
        {'praram':'foo','val':'2'},
        {'praram':'bar','val': '10'}
    ]
    return jsonify(results=list)

if __name__ == "__main__":
    app.run()
    

