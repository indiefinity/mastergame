from flask import Flask, render_template
import os
import json
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
        return "success"
@app.route('/join/<id>', methods = ['POST'])
def join(id):
    print(id)
    if os.path.exists('./games/' + id + ".json"):
        boolean = 1
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
    else:
        boolean = 0
    return str(boolean) 
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
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
