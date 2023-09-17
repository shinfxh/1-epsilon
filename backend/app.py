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
openai.api_key = ""
openAIengine = 'text-davinci-003'

def init():
    conn = sqlite3.connect('db.db')
    cursor = conn.execute("SELECT ID, NAME, ROLE, TALK, LIE from USER")
    userMap = dict()
    invUserMap = dict()
    lieMap = dict()
    talkMap = dict()
    for row in cursor:
        userMap[row[0]] = row[1]
        invUserMap[row[1]] = row[0]
        lieMap[row[1]] = row[4]
        talkMap[row[1]] = row[3]
        print(row[0], row[1])
    conn.close()
    return userMap, invUserMap, lieMap, talkMap

@app.route('/getMessages', methods = ['GET'])
def getSomeMessage():
    userMap, invUserMap, _, _ = init()
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

def getSomeMessageList(p1, p2):
    userMap, invUserMap, _, _ = init()
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
    return content

def promptGen(ls, responder, other, otherRole, lieMap=None, talkMap=None):

    if otherRole == "Blue":
        starting_prompt = f'''
        You are {other}. You are playing a game with other people. Everyone has roles assigned to them.
        You are a blue civilian. Your enemies are the red team.
        Your job is to protect the President from the Assassin.
        You should not reveal your role easily. You should collect information of other people and tell them to people on your team.
        Your personal traits: you lie {lieMap[other]}% of the time and your talkativeness is {talkMap[other]}%.
        '''
    elif otherRole == "Red":
        starting_prompt = f'''
        You are {other}. You are playing a game with other people. Everyone has roles assigned to them.
        You are a red civilian. Your enemies are the blue team.
        Your job is to help the Assassin to be in the same room as the President.
        You should not reveal your role easily. You should collect information of other people and tell them to people on your team.
        Your personal traits: you lie {lieMap[other]}% of the time and your talkativeness is {talkMap[other]}%.
        '''
    elif otherRole == "President":
        starting_prompt = f'''
        You are {other}. You are playing a game with other people. Everyone has roles assigned to them.
        You are assigned the role of President, the most important member of the blue team. Your enemy is the red team.
        You should not reveal that your identity to other players, unless you really trust that they are blue team.
        You do not want to be in the same room as the Assassin at the end of the game. If you think an Assassin is in the room, you should get Blue team to vote you out of the room.
        Your personal traits: you lie {lieMap[other]}% of the time and your talkativeness is {talkMap[other]}%.
        '''
        #
    elif otherRole == "Assassin":
        starting_prompt = f'''
        You are {other}. You are playing a game with other people. Everyone has roles assigned to them.
        You are assigned the role of Assassin, the most important member of the red team. Your enemy is the blue team.
        You should not expose your identity, unless you are really sure the other person is on red team.
        Your job is to be in the same room as the President at the end of the game. Try to remain or get voted into the same room as the President.
        Your personal traits: you lie {lieMap[other]}% of the time and your talkativeness is {talkMap[other]}%.
        '''
        # If the president is in the room, try to remain in the room. If you think the president is in the other room, try to get voted out of the current room.
    prompt = starting_prompt + """Now, you converse with {}. \n""".format(responder)
    for row in ls:
        prompt += """{}: {}\n""".format(row["sender"], row["content"])
    prompt += """{}:""".format(other)
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
    userMap, invUserMap, _, _ = init()
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
    userMap, invUserMap, _, _ = init()
    # args = request.args
    # response, responder, other = args['response'], args['responder'], args['other']
    conn = sqlite3.connect('db.db')
    cursor = conn.execute("""SELECT * from MESSAGE ORDER BY ID DESC LIMIT 1""")
    last_id = 0
    for row in cursor:
        print(row)
        last_id = int(row[0])
    print("responder = ", responder)
    print("other = ", other)
    sender_id = invUserMap[responder]
    receiver_id = invUserMap[other]
    conn.close()
    conn = sqlite3.connect('db.db')
    print('sender_id = ', sender_id)
    print("receiver_id = ", receiver_id)
    print(f"INSERT INTO MESSAGE (ID, SENDERID, RECEIVERID, CONTENT) \
      VALUES ({last_id + 1}, {sender_id}, {receiver_id}, \"{response}\")")
    conn.execute(f"INSERT INTO MESSAGE (ID, SENDERID, RECEIVERID, CONTENT) \
      VALUES ({last_id + 1}, {sender_id}, {receiver_id}, \"{response}\")")
    conn.commit()
    conn.close()

@app.route('/sendMessage', methods = ['POST'])
def sendMessage():
    data = request.json
    print("received {}".format(data))

    # 1. first, update DB
    updateDB(data["response"], data["responder"], data["other"])

    print("update DB success")

    # 2. get messages
    messagesList = getSomeMessageList(data["responder"], data["other"])
    print("messagesList", messagesList)

    # 3. get prompt
    userMap, invUserMap, lieMap, talkMap = init()
    prompt = promptGen(messagesList, data["responder"], data["other"], data["otherRole"], lieMap=lieMap, talkMap=talkMap)
    print("prompt", prompt)
    
    # 4. get completion
    completion = complete(prompt, None, data["other"]).strip()

    print("completion = ", completion)

    # 5. get the completion into the dataset
    updateDB(completion, data["other"], data["responder"])

    resp = "received"
    return resp