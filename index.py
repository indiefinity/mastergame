from flask import Flask, render_template
import os
import json
import random as ran
app = Flask(__name__, template_folder='./')
@app.route("/")
def index():
    return render_template('index.html')
@app.route('/create/<id>', methods = ['POST'])
def create(id):
    print(id)
    if os.path.exists('./games/' + id):
        return "error"
        #handled on client
    else:
        f = open("./games/" + id + ".json", "w+")
        f.write('{"id":' + id + ',"playercount":1}')
        f.close()
        f = open("./games/" + id + ".json","r")
        data = f.read()
        f.close()
        jsonObj = json.loads(data)
        jsonObj["started"] = False
        jsonObj["q"] = '{"q":"If you were a car would you prefer to be","a":"White?","a2":"Black?","a3":"Gray?", "a4":"Yellow?"}'
        f = open("./games/" + id + ".json","w")
        f.seek(0)
        f.write(json.dumps(jsonObj))
        f.close()
        return "success"
@app.route('/join/<id>', methods = ['POST'])
def join(id):
    print(id)
    if os.path.exists('./games/' + id + ".json"):
        f = open("./games/" + id + ".json","r")
        data = f.read()
        f.close()
        jsonObj = json.loads(data)
        jsonObj["playercount"] = jsonObj["playercount"] + 1
        f = open("./games/" + id + ".json","w")
        f.seek(0)
        f.write(json.dumps(jsonObj))
        print(jsonObj)
        f.close()
        return "exists"
    else:
        return "error" 
@app.route('/start/<id>', methods = ['POST'])
def  start(id):
    f = open("./games/" + id + ".json","r")
    data = f.read()
    f.close()
    jsonObj = json.loads(data)
    jsonObj["started"] = True
    f = open("./games/" + id + ".json","w")
    f.seek(0)
    f.write(json.dumps(jsonObj))
    f.close()
    return "started" + id
@app.route('/ready/<id>', methods = ['POST'])
def  ready(id):
    f = open("./games/" + id + ".json","r")
    data = f.read()
    f.close()
    jsonObj = json.loads(data)
    if jsonObj["started"]:
        return "started"
    else:
        return "not yet"
@app.route('/client/<id>', methods = ['POST'])
def client(id):
    f = open("./games/" + id + ".json","r")
    data = f.read()
    f.close()
    jsonObj = json.loads(data)
    return jsonObj["q"]
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
