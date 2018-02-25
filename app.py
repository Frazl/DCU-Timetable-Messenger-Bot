import os, sys
from flask import Flask, request
from pymessenger import Bot
import bs4dcu

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "ACCESSTOKENHERE"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "VERIFYTOKENHERE":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "OK", 200

@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)
	response = ""
	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:
				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
						if messaging_text[:5] == "!next":
								x = messaging_text
								x = x.split()
								if len(x) > 1:
										code = x[1]
										response = bs4dcu.next(code)
										response = bs4dcu.responsehandler(response)
								else:
									response = bs4dcu.next()
									try:
										response = bs4dcu.responsehandler(response)
									except IndexError: 
										response = "Nothing On"
								if response == "":
									response = "Nothing On"	
						elif messaging_text[:6] == "!today":
							print("Said !today")
							x = messaging_text
							x = x.split()
							if len(x) > 1:
								code = x[1]
								response = bs4dcu.run("Mon", None, code)
								response = bs4dcu.dictionaryhandler(response)
								print(response)
							else:
								response = bs4dcu.run("Mon")
								response = bs4dcu.dictionaryhandler(response)
					else:
						response = 'Nothing Received...'
					# Echo
					# response = messaging_text
					bot.send_text_message(sender_id, response)
	return "OK", 200

def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 80)