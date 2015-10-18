import json
import gspread
import ast
from oauth2client.client import SignedJwtAssertionCredentials
from twilio.rest import TwilioRestClient

# Initiate Twilio Client
account = 'TWILIO_ACCOUNT'
token = 'TWILIO_TOKEN'
myNumber = 'TWILIO_NUMBER'

client = TwilioRestClient(account, token)

# load old game list
gameBook = open("allGames.paw", "r+b")
games = ast.literal_eval(gameBook.read())

# sign into spreadsheet and load values

json_key = json.load(open("gspread.json", 'r'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
gc = gspread.authorize(credentials)

wks = gc.open("GOOGLE SPREADSHEET TITLE").sheet1

# Iterate through games in worksheet
# check for entries not inside of games array
newGames = [];
for game in wks.get_all_values():
	if ( game != ['', '', '','']):
		if game not in games:
			newGame = "NEW: " + game[0]  + " " + game[1]  + " " + game[2]  + " " + game[3] 	
			games.append(game)
			newGames.append(newGame)
		else:
			oldGame = "OLD: " + game[0]  + " " + game[1]  + " " + game[2]  + " " + game[3] 	
			newGames.append(oldGame)

# Write game archive (with any changes)
gameBook.seek(0)
gameBook.write(str(games))		
gameBook.truncate()
gameBook.close()


try:
	print(str(newGames))
    
except twilio.TwilioRestException as e:
    print e


