import requests,random
from flask import Flask, request

app = Flask(__name__)

page_token = "YOUR_TOKEN"
token_authorization = "test_token"
list_text = ["สวัสดี มีอะไรมั้ยพอดีแอดมินหลับอยู่","ว่าไง","เพจ Dev แบบกล้วยๆ เอง"]


@app.route('/webhook',methods=['GET'])
def webhook_authorization():
    verify_token = request.args.get("hub.verify_token")
    if verify_token == token_authorization:
        return request.args.get("hub.challenge")
    return 'Unable to authorize.'

@app.route("/webhook", methods=['POST'])
def callback():
    data = request.get_json()
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
                'recipient': {
                    'id': sender_id
                },
                'message': {"text":random.choice(list_text)}
            }
        response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+page_token,json=request_body).json()
    return response


if __name__ == "__main__":
    app.run(threaded=True, port=8000)