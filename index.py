from flask import Flask, render_template
import os
import json
q = "q"
from random import randint
from flask_socketio import *
app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
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
        if randint(1,2) == 1:
            qf = open("./questions/style1.json")
        else:
            qf = open("./questions/style2.json")
        qjson = json.loads(qf.read())
        qf.close
        global q
        q = qjson["q"]
        q2= qjson["q2"]
        s = qjson["s"][randint(0,len(qjson["s"]) - 1)]
        a1 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        a2 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        a3 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        a4 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        while a1 == a2 or a1 == a3 or a1 == a4 or a2 == a3 or a2 == a4 or a3 == a4:
            a1 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
            a2 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
            a3 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
            a4 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        fq = q + s + q2
        finalq = '{"q":"%s","a":"%s","a2":"%s","a3":"%s", "a4":"%s"}' % (fq, a1, a2, a3, a4)
        print(q+s+q2+a1+a2+a3+a4)
        print(finalq)
        jsonObj = json.loads(data)
        jsonObj["started"] = False
        jsonObj["q"] = finalq
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
    aturn  = "m"
    socketio.emit('gamestart', True)
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
@app.route('/select/<id>/<selection>', methods = ['POST'])
def select(id, selection):
    #en jaksa nyt kek
    return "homo"
@app.route('/ville/<id>', methods = ['POST'])
def ville(id):
    print("ville")
    winsound.Beep(600, 250)
    return "beeped"
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')
@socketio.on('getq')
def getq():
    socketio.emit('q', q)
@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
def newq(id):
    if True:
        global q
        f = open("./games/" + id + ".json","r")
        data = f.read()
        f.close()
        if randint(1,2) == 1:
            qf = open("./questions/style1.json")
        else:
            qf = open("./questions/style2.json")
        qjson = json.loads(qf.read())
        qf.close
        q = qjson["q"]
        q2= qjson["q2"]
        s = qjson["s"][randint(0,len(qjson["s"]) - 1)]
        a1 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        a2 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        a3 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        a4 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        while a1 == a2 or a1 == a3 or a1 == a4 or a2 == a3 or a2 == a4 or a3 == a4:
            a1 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
            a2 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
            a3 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
            a4 = qjson["a"][randint(0,len(qjson["a"]) - 1)]
        fq = q + s + q2
        finalq = '{"q":"%s","a":"%s","a2":"%s","a3":"%s", "a4":"%s"}' % (fq, a1, a2, a3, a4)
        print(q+s+q2+a1+a2+a3+a4)
        print(finalq)
        jsonObj = json.loads(data)
        jsonObj["q"] = finalq
        f = open("./games/" + id + ".json","w")
        f.seek(0)
        f.write(json.dumps(jsonObj))
        f.close()
if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0')
    socketio.run(app,debug=True,host='0.0.0.0', port='80')
