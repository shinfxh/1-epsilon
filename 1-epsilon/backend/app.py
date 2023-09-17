from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import sqlite3
import re

app = Flask(__name__)
CORS(app)

openAIEnabled = True
openai.api_key = "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"
openAIengine = 'text-davinci-003'

conn = sqlite3.connect('db.db')
cursor = conn.execute("SELECT ID, NAME, ROLE, TALK, LIE from USER")
userMap = dict()
invUserMap = dict()
for row in cursor:
    userMap[row[0]] = row[1]
    invUserMap[row[1]] = row[0]
conn.close()

def getSomeMessage(sender, receiver):
    conn = sqlite3.connect('db.db')
    a = invUserMap[sender]
    b = invUserMap[receiver]
    cursor = conn.execute("""SELECT ID, SENDERID, RECEIVERID, CONTENT from MESSAGE WHERE SENDERID={} AND RECEIVERID={} OR SENDERID={} AND RECEIVERID={}""".format(a, b, b, a))
    content = []
    for row in cursor:
        content.append({
            "sender" : userMap[row[1]],
            "receiver" : userMap[row[2]],
            "content": row[3]
        })
    conn.close()
    return content