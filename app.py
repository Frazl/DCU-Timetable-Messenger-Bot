import os, sys
from flask import Flask, request
from pymessenger import Bot
import bs4dcu

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAADAkzBKVHABADJ7vNYyMrY5TDUOXv9OHZA3ZAXWJmpK4hzjCxIPqkLpgGLzbfpaK8vWUqjKJc4BBWqwwATwJ0xAnTeYMcZC9ZBLtB9kongYXZBdYCMYMKDmCWjF6tLBH2Jx0jIork7d0tgK8BmPmDxB2kZAZClSBNjeeGb59AFOwZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)


#Time Check
def timecheck(s):
    	if s.lower() == "none":
    			return None
    	else:
    			return s

# User Functions
def isuser(sid):
	with open("userinfo.txt") as file:
		for x in file:
			l = x.split(":")
			if l[0] == sid:
    				return True
	return False

def updateuser(sid, code, year):
    with open("userinfo.txt", "r+") as file:
        d = file.readlines()
        file.seek(0)
        for x in d:
            l = x.split(":")
            if l[0] != sid:
                file.write(x)
        file.write(sid+":"+code+":"+year+"\n")
        file.truncate()
        file.close

def userinfo(sid):
	with open("userinfo.txt") as file:
		for x in file:
			l = x.split(":")
			code = l[1]
			year = l[2]
	return code, year
			

@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
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
				#recipient_id = messaging_event['recipient']['id']
				
				#Get UserInfo
				usercheck = isuser(sender_id)
				if usercheck:
    					code, year = userinfo(sender_id)
    					year = year.strip()
    					print(code, year)
				time = None
				#Message Handling
				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text'].lower()
						print("Got Text Message!")
						#!next Event
						if messaging_text[:4] == "next":
								x = messaging_text
								x = x.split()
								if len(x) > 2:
										code = x[1].upper()
										year = x[2]
										response = bs4dcu.next(code, year)
								elif usercheck:
										response = bs4dcu.next(code, year)
								if response == "":
									response = "Nothing On Next"	
						#!today Event
						elif messaging_text[:5] == "today":
							x = messaging_text
							x = x.split()
							if len(x) > 2:
								code = x[1].upper()
								year = x[2]
								response = bs4dcu.gettoday(code, year)
								response = bs4dcu.dictionaryhandler(response)
							elif usercheck:
								response = bs4dcu.gettoday(code, year)
								response = bs4dcu.dictionaryhandler(response)
						#ON Event
						elif messaging_text[:2] == "on":
							try:
								x = messaging_text
								x = x.split()
								#Search
								if len(x) == 5:
									print("Running This!...")
									day = x[1].title()
									time = timecheck(x[2])
									code = x[3].upper()
									year = x[4]
									response = bs4dcu.run(day, time, code, year)
									if time == None:
    										response = bs4dcu.dictionaryhandler(response)
									else:
											response = bs4dcu.responsehandler(response)
								#User - Day Given
								elif usercheck and len(x) == 2:
									day = x[1].title()
									response = bs4dcu.run(day, None, code, year)
									response = bs4dcu.dictionaryhandler(response)
								#User - Time Given
								elif usercheck and len(x) == 3:
									day = x[1].title()
									time = x[2]
									response = bs4dcu.run(day, time, code, year)
									response = bs4dcu.responsehandler(response)
								else:
    									response = "Unsupported On Attributes"
							except:
								response = "Error Running On Command :("
						#!config Event
						elif messaging_text[:3] == "set":
								x = messaging_text.split()
								if len(x) == 3:
										code = x[1].upper()
										year = x[2]
										if not usercheck:
											with open("userinfo.txt", "a") as file:
												file.write(sender_id+":"+code+":"+year+"\n")
											response = "Set your config! :)"
										else:
											updateuser(sender_id, code, year)
											response = "Updated your config! :)"
								else:
									response = "Format should be !config CODE YEAR"
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