import flask
import pika
from flask import request, jsonify
import logging
import json
import sqlite3
#import pydblite
#from pydblite import Base

#file = "friends.txt"

logging.basicConfig(filename='app.log',level=logging.DEBUG
                    ,format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "<h1>ESD</h1><br><h1>Name: Pokpong Rujuirachartkul</h1>"

@app.route('/api/v1/resource/friends/all', methods=['GET'])
def api_all():
    friends = []
    conn = sqlite3.connect('friend.sqlite')
    c = conn.cursor()
    cursor = conn.execute("SELECT id, name, track from friends")
    for i in cursor:
        friends.append(i)
    return jsonify(friends)    
    #Old - Pydblite
    '''
    friends = []
    db = Base('friends', save_to_file=True)
    if db.exists():
        db.open()
    else:
        db.create('id','name','track')
    for i in db:
        friends.append(i)
    
    #print(friends)
    return jsonify(friends)
    '''
@app.route('/api/v1/resource/friends_id', methods=['GET'])
def api_id():
    #Sqlite
    if('id' in request.args):
        id = int(request.args['id'])
    else:
        return "Error : No id provided. Please specify an id"

    friends = []
    conn = sqlite3.connect('friend.sqlite')
    c = conn.cursor()
    cursor = conn.execute("SELECT * FROM friends WHERE id=?",(id,))
    for i in cursor:
        friends.append(i)
    return jsonify(friends)   
    #Old - Text file
    '''
    friends = []
    with open(file) as f:
        z = f.read().splitlines()

    for i in z:
        friends.append(json.loads(str(i)))
        
    if('id' in request.args):
        id = int(request.args['id'])
    else:
        return "Error : No id provided. Please specify an id"
    result = []

    for friend in friends:
        if friend['id'] == id:
            result.append(friend)

    return jsonify(result)
    '''
    #Old - Pydblite
    '''
    friends = []
    db = Base('friends', save_to_file=True)
    if db.exists():
        db.open()
    else:
        db.create('id','name','track')
    
    if('id' in request.args):
        id = int(request.args['id'])
    else:
        return "Error : No id provided. Please specify an id"

    for i in (db('id') == str(id)):
        friends.append(i)

    return jsonify(friends)
    '''
@app.route('/api/v1/resource/friends_name', methods=['GET'])
def api_name():
    #Sqlite
    if('name' in request.args):
        name = request.args['name']
    else:
        return "Error : No name provided. Please specify name"

    friends = []
    conn = sqlite3.connect('friend.sqlite')
    c = conn.cursor()
    cursor = conn.execute("SELECT * FROM friends WHERE name=?",(name,))
    for i in cursor:
        friends.append(i)
    return jsonify(friends)   
    #Old - Text file
    '''
    friends = []
    with open(file) as f:
        z = f.read().splitlines()

    for i in z:
        friends.append(json.loads(str(i)))
        
    if('name' in request.args):
        name = request.args['name']
    else:
        return "Error : No name provided. Please specify name"
    result = []

    for friend in friends:
        if friend['name'] == name:
            result.append(friend)

    return jsonify(result)
    '''
    #Old - Pydblite
    '''
    friends = []
    db = Base('friends', save_to_file=True)
    if db.exists():
        db.open()
    else:
        db.create('id','name','track')
    
    if('name' in request.args):
        name = request.args['name']
    else:
        return "Error : No name provided. Please specify name"

    for i in (db('name') == str(name)):
        friends.append(i)
    
    return jsonify(friends)
    '''

@app.route('/api/v1/resource/friends_track', methods=['GET'])
def api_track():
    #Sqlite
    if('track' in request.args):
        track = request.args['track']
    else:
        return "Error : No name provided. Please specify track"

    friends = []
    conn = sqlite3.connect('friend.sqlite')
    c = conn.cursor()
    cursor = conn.execute("SELECT * FROM friends WHERE track=?",(track,))
    for i in cursor:
        friends.append(i)
    return jsonify(friends)
    #Old - Text file
    '''
    friends = []
    with open(file) as f:
        z = f.read().splitlines()

    for i in z:
        friends.append(json.loads(str(i)))

    if('track' in request.args):
        track = request.args['track']
    else:
        return "Error : No track provided. Please specify track"
    result = []

    for friend in friends:
        if friend['track'] == track:
            result.append(friend)

    return jsonify(result)     
    '''
    #Old - Pydblite
    '''
    friends = []
    db = Base('friends', save_to_file=True)
    if db.exists():
        db.open()
    else:
        db.create('id','name','track')
    
    if('track' in request.args):
        track = request.args['track']
    else:
        return "Error : No name provided. Please specify track"

    for i in (db('track') == str(track)):
        friends.append(i)
    
    return jsonify(friends)
    '''
@app.route('/api/v1/resource/friends/add', methods=['GET'])
def api_add():
    #Connect to RabbitMQ

    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq',5672,'/',pika.PlainCredentials('guest','guest')))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
        
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    #channel = connection.channel()
    #channel.queue_declare(queue='task_queue',durable=True)

    temp = ''
    name = ''
    id = 0
    track = ''
    a = 0
    if('name' in request.args):
        name = request.args['name']
        a+=1
    if('id' in request.args):
        id = request.args['id']
        a+=1
    if('track' in request.args):
        track = request.args['track']
        a+=1
    if(a==3):
        temp = "{\"id\" : "+str(int(id))+",\"name\" : \""+name+"\",\"track\" : \""+track+"\"}"

    conn = sqlite3.connect('friend.sqlite')
    c = conn.cursor()
    conn.execute("INSERT INTO friends (ID,NAME,TRACK) \
      VALUES (?,?,?)",(int(id),name,track));
    conn.commit()
    conn.close() 

    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body = temp,
                          properties=pika.BasicProperties(delivery_mode=2,))
            
    
    connection.close()
    print("[x] Sent: %s"%temp)
    return "<h1>Successfully added!</h1>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
