from flask import Flask, request, jsonify, render_template, Blueprint
from firebase_functions import https_fn

import requests
import json
import os

line_bp = Blueprint('line', __name__)

ACCESS_TOKEN = "TEST_TOKEN"
# test chat group id, via webhook.site to get the group id
GROUP_ID = "GROUP_ID_YOU_WANT_TO_PUSH_TO"

LINE_BOT_PUSH_URL = "https://api.line.me/v2/bot/message/push"
LINE_BOT_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
GEMINI_API_KEY = "YOUR_OWN_API_KEY"

XAI_URL = "https://api.x.ai/v1/completions"
XAI_API_KEY = "YOUR_OWN_API_KEY"


@line_bp.route('/line', methods=['GET', 'POST'])
def handle_line_webhook():
    if request.method == 'POST':
        # This is where you would handle an incoming webhook from LINE
        # For example, get the JSON body of the request
        received_data = request.get_json()
        # Your logic to process the webhook data goes here...
        text_value = received_data['events'][0]['message']['text']
        # desination to get where you want to reply to
        destination = received_data['events'][0]['replyToken']
        handle_msg(text_value, destination)
        
        return jsonify({'status': 'success'}), 200
    elif request.method == 'GET':
        return "<h1>This is the endpoint for the hook.</h1>", 200

def handle_msg(msg, dest):
    if 'triston' in msg.lower():
        print(f'Hello Trison!')
        linebot_msg('{hat2} Hello, Triston!', dest, True)

    if 'joanne' in msg.lower():
        print(f'Hello Joanne!')
        linebot_msg('{hat1} Hello, Joanne! {hbd1} {hbd2}', dest, True)

    if msg.lower().startswith('ai '):
        query = msg[3:len(msg)]
        print(f'AI checking! {query}')
        linebot_msg(gemini_request(query), dest, False)
        
    if msg.lower().startswith('xai '):
        query = msg[3:len(msg)]
        print(f'AI checking! {query}')
        linebot_msg(xai_request(query), dest, False)

def xai_request(msg):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {XAI_API_KEY}"
    }
    
    data = {
        "model": "grok-beta", "prompt": msg, "max_tokens": 50
    }
    
    try:
        response = requests.post(XAI_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes
        # To-Do: parse the output format of XAI
        #answer = response.json()['candidates'][0]['content']['parts'][0]['text']
        print(f'{response}')
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    
    return response

def gemini_request(msg):
    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        "contents": [
            {
                "parts": [{"text": msg}]
            }
        ]
    }

    params = {
        "key": GEMINI_API_KEY
    }
    
    try:
        response = requests.post(GEMINI_URL, headers=headers, params=params, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes
        answer = response.json()['candidates'][0]['content']['parts'][0]['text']
        print(f'{answer}')
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")
    
    return answer

def linebot_msg(msg, dest, emoji=False):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    if emoji:
        data = {
    # To push msg
    #	    "to": GROUP_ID,
    # To reply msg 
            "replyToken": dest,
            "messages": 
            [
                {
                    "type": "textV2", 
                    "text": msg,
                    "substitution": 
                    {
                        "hat1": 
                        {
                             "type": "emoji",
                             "productId": "5ac2213e040ab15980c9b447",
                             "emojiId": "006"
                        },
                        "hat2": 
                        {
                             "type": "emoji",
                             "productId": "5ac2213e040ab15980c9b447",
                             "emojiId": "005"
                        },
                        "hbd1": 
                        {
                             "type": "emoji",
                             "productId": "5ac2213e040ab15980c9b447",
                             "emojiId": "010"
                        },
                        "hbd2": 
                        {
                             "type": "emoji",
                             "productId": "5ac2213e040ab15980c9b447",
                             "emojiId": "048"
                        }
                    }
                }
            ]
        }
    else:
        data = {
    # To push msg
    #	"to": GROUP_ID,
    # To reply msg 
            "replyToken": dest,
            "messages": [
                {
                     "type": "text", 
                     "text": msg
                }
            ]
        }        
    
    response = requests.post(LINE_BOT_REPLY_URL, json=data, headers=headers)

