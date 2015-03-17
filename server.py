import psycopg2
import psycopg2.extras
import os
import uuid
from flask import Flask, session
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

messages = [{'text':'test', 'name':'testName'}]
users = {}
searches = [{'text':'test', 'name':'testName'}]

def connectToDB():
  connectionString = 'dbname=messageboard user=postgres password=postgres host=localhost'
  try:
    return psycopg2.connect(connectionString)
  except:
    print("Can't connect to database")
    
    

def updateRoster():
    names = []
    for user_id in  users:
        print users[user_id]['username']
        if len(users[user_id]['username'])==0:
            names.append('Anonymous')
        else:
            names.append(users[user_id]['username'])
    print 'broadcasting names'
    emit('roster', names, broadcast=True)
    

@socketio.on('connect', namespace='/chat')
def test_connect():
    session['uuid']=uuid.uuid1()
    print 'uuid is ', session['uuid']
    session['username']='starter name'
    print 'connected'
    
    users[session['uuid']]={'username':'New User'}
   # updateRoster()


    #for message in messages:
     #   emit('message', message)

@socketio.on('message', namespace='/chat')
def new_message(message):
    #tmp = {'text':message, 'name':'testName'}
    tmp = {'text':message, 'name':users[session['uuid']]['username']}
    messages.append(tmp)
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    try:
       
      cur.execute("""INSERT INTO messages (username, message) VALUES (%s, %s);""",
       (users[session['uuid']]['username'], message)) 
    except:
      print("ERROR inserting into messages")
    conn.commit()
    
    emit('message', tmp, broadcast=True)
    
@socketio.on('identify', namespace='/chat')
def on_identify(message):
    print 'identify' + message
    users[session['uuid']]={'username':message}
    
    updateRoster()
    
    
@socketio.on('login', namespace='/chat')
def on_login(pw):
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if user typed in a post ...
    try:
       
      cur.execute("""INSERT INTO users (username, password) VALUES (%s, %s);""",
       (users[session['uuid']]['username'], pw)) 
    except:
      print("ERROR inserting into users")
    conn.commit()
    
       
    updateRoster()


    for message in messages:
        emit('message', message)
    
    print 'login '  + pw
    
    #users[session['uuid']]={'username':message}
    #updateRoster()
    
    
@socketio.on('search', namespace='/chat')
def on_search(search):
    
    
    conn = connectToDB()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    print 'searching '  + search
    
    try:
       query= "SELECT * from messages WHERE message LIKE '%%%s%%';"%(search) 
       cur.execute(query)
    except:
      print("Error searching")
    cur.execute(query)
    row = cur.fetchall()
    print row 

   # emit('search', row) 
    for search in row:
        tmp = {'text':search[1], 'name':search[0]}
        emit('search', tmp)
    
    
    #users[session['uuid']]={'username':message}
    #updateRoster()


    
@socketio.on('disconnect', namespace='/chat')
def on_disconnect():
    print 'disconnect'
    if session['uuid'] in users:
        del users[session['uuid']]
        updateRoster()

@app.route('/')
def hello_world():
    print 'in hello world'
 #   conn = connectToDB()
  #  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   # rows=[]
    #search= request.form['search']
    #query= "SELECT * FROM messages WHERE message LIKE '%%%s%%';" % (search)
    #cur.execute(query)
    #rows= cur.fetchall()
    
    return app.send_static_file('index.html')
    return 'Hello World!'

@app.route('/js/<path:path>')
def static_proxy_js(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('js', path))
    
@app.route('/css/<path:path>')
def static_proxy_css(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('css', path))
    
@app.route('/img/<path:path>')
def static_proxy_img(path):
    # send_static_file will guess the correct MIME type
    return app.send_static_file(os.path.join('img', path))
    
if __name__ == '__main__':
    print "A"

    socketio.run(app, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
     
