from flask import Flask
from flask import jsonify
import json

app = Flask(__name__)

users = {"1":"abc","2":"def"}

@app.route("/")
def hello():
    dic = {}
    dic.keys()
    print(dic)
    return json.dumps(users)

@app.route("/restful")
def restful():
    return jsonify(results=users)

if __name__ == "__main__":
    app.run()
