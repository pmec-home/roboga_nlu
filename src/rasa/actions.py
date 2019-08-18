# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json
from rasa_core_sdk import Action
from rasa_core_sdk.endpoint import *
import pandas as pd
import spacy
import os
import re
from datetime import datetime

logger = logging.getLogger(__name__)
directory = os.path.dirname(os.path.realpath(__file__))

import sys
current_module = sys.modules[__name__]

###########################################################
# List of Intens
# AWALYS CHANGE THIS LIST WHEN ,ADD A NEW INTENT, OR CHANGE AN INTENT NAME
##########################################################
from enum import Enum
class Intents(Enum):
	MOVE = 'move'
	GREET = 'greet'
	QUESTION = 'question'
	

###########################################################
# Initilize some global variables
# the list of questions and answer and its nlp abstraction
##########################################################
#Questions and Answer dataset
QandA = pd.read_csv(directory+'/questions_and_answers.csv')
nlp = spacy.load('en_core_web_sm')
def load_nlp(word_list):
    global nlp
    nlp_list = []
    for word in word_list:
        nlp_list.append(nlp(str(word), 'utf8'))
    return nlp_list

def compareToNlpList(phrase, nlp_list):
    global nlp
    nlp_phrase = nlp(phrase)
    ranks = []
    for element in nlp_list:
        ranks.append({})
        ranks[-1]['text'] = element.text
        ranks[-1]['similarity'] = nlp_phrase.similarity(element)
    return sorted(ranks, key=lambda x: x['similarity'], reverse=True)
nlp_list = load_nlp(QandA['QUESTION'])
#The database

###########################################################
# Actions classes
############################################################

#'tracker' object reference: https://rasa.com/docs/core/api/tracker/
#'dispatcher' object reference: https://rasa.com/docs/core/api/dispatcher/

class ActionPlanner(Action):
	def name(self):
		# define the name of the action which can then be included in training stories
		return "action_planner"

	def run(self, dispatcher, tracker, domain):
		#print(json.dumps(tracker.current_state(), indent=2))
		message = tracker.latest_message['text']
		intent = Intents(tracker.latest_message["intent"].get("name"))
		entities = [{"entity": x.get("entity"), "value": x.get("value")} for x in tracker.latest_message.get("entities")]		
		
		message_back = "Your message intent: \"{}\" , extracted entities: {}".format(intent,entities)
		dispatcher.utter_message(message_back)  # send the message back to the user
		return []

class ActionAnswerQuestion(Action):
	def name(self):
		# define the name of the action which can then be included in training stories
		return "action_answer_question"

	def run(self, dispatcher, tracker, domain):
		global nlp_list, QandA
		
		message = tracker.latest_message['text']
		intent = Intents(tracker.latest_message["intent"].get("name"))
		
		if(intent == Intents.QUESTION):
			rank = compareToNlpList(message, nlp_list)
			if(float(rank[0]['similarity']) > 0.65):
				#Grab answer form the Q and A dataframe
				answer = QandA[QandA['QUESTION'] == rank[0]['text']]['ANSWER'].iloc[0]
				#If the answer is in the format ${code} grab the code inside and run ir
				if '$' in answer:
					code = re.search('\${(.*)}', answer).group(1)
					answer = eval(code)
				dispatcher.utter_message(answer)
				return []
			
		dispatcher.utter_message('Sorry I did not undestand your question')
		return []	
	
class ActionExecuter(Action):
	def name(self):
		# define the name of the action which can then be included in training stories
		return "action_execute_plan"

	def run(self, dispatcher, tracker, domain):
		intent = tracker.latest_message["intent"].get("name")
		if(intent == "affirm"):
			dispatcher.utter_message('Executing the message')  # send the message back to the user
			#send command to robot
		else:
			dispatcher.utter_message('Ok, I will be waiting for your command')  # send the message back to the user
		return []

#Helper function to initilize an action server from the .py
def run_action_server(port=DEFAULT_SERVER_PORT, cors='*'):
	print("Starting action endpoint server...")
	edp_app = endpoint_app(cors_origins=cors,
							action_package_name=current_module)

	http_server = WSGIServer(('0.0.0.0', port), edp_app)

	http_server.start()
	print("Action endpoint is up and running. on {}"
				"".format(http_server.address))

	http_server.serve_forever()

if __name__ == "__main__":
	run_action_server()

