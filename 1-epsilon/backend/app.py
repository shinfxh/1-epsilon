from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import sqlite3
import re
import sqlite3
import numpy as np
import openai
conn = sqlite3.connect('db.db')

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
    print(row[0], row[1])
conn.close()

@app.route('/getMessages', methods = ['GET'])
def getSomeMessage():
    args = request.args
    p1, p2 = args['p1'], args['p2']
    print(p1, p2)
    conn = sqlite3.connect('db.db')
    a = invUserMap[p1]
    b = invUserMap[p2]
    print(a, b)
    cursor = conn.execute("""SELECT ID, SENDERID, RECEIVERID, CONTENT from MESSAGE WHERE SENDERID={} AND RECEIVERID={} OR SENDERID={} AND RECEIVERID={}""".format(a, b, b, a))
    content = []
    for row in cursor:
        content.append({
            "sender" : userMap[row[1]],
            "receiver" : userMap[row[2]],
            "content": row[3]
        })
    conn.close()
    print("DONE HERE!")
    print(content)
    return jsonify(content)

def promptGen(ls, responder, other):
    starting_prompt = f'''
    You are {responder}. You are playing a game with other people. Everyone has roles assigned to them.
    You are assigned the role of Civilian. 
    Your job is to protect the President from the Assassin.
    '''
    prompt = starting_prompt + """Here is a conversation between you and {}. \n""".format(other, other)
    for row in ls:
        prompt += """{}: {}\n""".format(row["sender"], row["content"])
    prompt += """{}:""".format(responder)
    return prompt

def parser(complete, other):
    return complete.split("{}:".format(other))[0]

def complete(prompt, bot, player): #always used on bot
    if openAIEnabled:
        completion = openai.Completion.create(engine = openAIengine, prompt = prompt).choices[0].text.rstrip()
        #app.logger.warning("in completion - {}".format(completion))
        retry = 0
        endToken = {'.', '?', '!'}
        curprompt = prompt
        while retry < 2 and completion[-1] not in endToken:
            retry += 1
            curprompt = prompt + completion
            completion += openai.Completion.create(engine=openAIengine, prompt=curprompt).choices[0].text.rstrip()
        return parser(completion, player)
    else:
        return "Sorry, I didn't catch what you said. Could you repeat that again?"
    
def updateProbabilities(ls, p1, p2):
    #p2 last said something to p1, p1 updates their probabilities of p2
    a = invUserMap[p1]
    b = invUserMap[p2]
    conn = sqlite3.connect('db.db')
    cursor = conn.execute("SELECT PERCEIVER_ID, PERCEIVED_ID, P_PRESIDENT, P_CIVILIAN, P_ASSASSIN from PROB WHERE PERCEIVER_ID = {} AND PERCEIVED_ID = {}".format(a, b))
    initial = [0, 0, 0] #president, civilian, assassin
    for row in cursor:
        initial = row[2:]
    prompt = promptGen(ls[-1], responder = player, other = bot)
    prompt += f'Up to this point, the probabilities of {bot} being President, Civilian, Assassin are: {initial[0]}, {initial[1]}, {initial[2]} \n'
    prompt += 'Below is the most recent conversation: '
    prompt += """{}: {}\n""".format(ls[-1]["sender"], ls[-1]["content"])
    prompt += f'The updated probabilities {bot} being President, Civilian, Assassin are: '
    new_prob = openai.Completion.create(engine = openAIengine, prompt = prompt).choices[0].text.rstrip()
    new_prob = new_prob.split('\n')[0]
    if new_prob[-1] == '.':
        new_prob = new_prob[:-1]
    new_prob = new_prob.split(',')
    new_prob = [float(x) for x in new_prob]
    conn.execute(f"INSERT INTO PROB (PERCEIVER_ID, PERCEIVED_ID, P_PRESIDENT, P_CIVILIAN, P_ASSASSIN) \
    VALUES ({a}, {b}, {new_prob[0]}, {new_prob[1]}, {new_prob[2]})")
    conn.close()
    return new_prob

def updateDB(response, responder, other):
    # args = request.args
    # response, responder, other = args['response'], args['responder'], args['other']
    conn = sqlite3.connect('db.db')
    cursor = conn.execute("""SELECT ROW from MESSAGE ORDER BY ID DESC LIMIT 1""")
    last_id = cursor['ID']
    sender_id = invUserMap[responder]
    receiver_id = invUserMap[other]
    conn.execute(f"INSERT INTO MESSAGE (ID, SENDERID, RECEIVERID, CONTENT) \
      VALUES ({last_id + 1}, {sender_id}, {receiver_id}, {response})")
    conn.close()
