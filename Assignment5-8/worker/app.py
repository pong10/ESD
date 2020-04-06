import pika
from flask import request, jsonify
import logging
import json
import time
import re
import sqlite3
#import pydblite
#from pydblite import Base

sleepTime = 20
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(sleepTime)

print(' [*] Connecting to server ...')
#connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
#channel = connection.channel()
#channel.queue_declare(queue='task_queue', durable=True)


connection = pika.BlockingConnection(
    pika.ConnectionParameters('rabbitmq',5672,'/',pika.PlainCredentials('guest','guest')))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

print(' [*] Waiting for messages.')
#Test DB Connection

#pydblite
'''
db = Base('friends', save_to_file=True)
if db.exists():
    db.open()
else:
    db.create('id','name','track')
'''
#sqlite
conn = sqlite3.connect('friend.sqlite')
c = conn.cursor()

def callback(ch,method,properties,body):
    #Get value from Message Body
    print("[x] Received %s" % body)
    temp = str(body)
    temp = temp[2:-1]
    a = re.split(r'\s',temp)
    fid = a[2][:-7]
    fn = a[4][:-8].split('"')
    
    fn = fn[1]
    ft = a[6][:-1].split('"')
    
    ft = ft[1]
    
    #sqlite
    conn = sqlite3.connect('friend.sqlite')
    c = conn.cursor()
    conn.execute("INSERT INTO friends (ID,NAME,TRACK) \
      VALUES (?,?,?)",(int(fid),fn,ft));
    conn.commit()
    conn.close()  
    #pydbllite
    '''
    db = Base('friends', save_to_file=True)
    if db.exists():
        db.open()
    else:
        db.create('id','name','track')

    db.insert(fid,fn,ft)
    db.commit()
    '''
    #Mysql
    '''
    mydb = mysql.connector.connect(
    host = "localhost",
    user = "Pong",
    passwd = "1234567890",
    database="esdhw")

    mycursor = mydb.cursor()

    sql = "insert into friends (Friend_ID,Name,Track) values (%s,%s,%s)"
    val = (int(fid),fn,ft)
    
    mycursor.execute(sql,val)
    mydb.commit()
    '''
    print("[x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1) #limit the no. of unacknowledge messages
channel.basic_consume(queue='task_queue',
                     on_message_callback=callback)
channel.start_consuming()
    
