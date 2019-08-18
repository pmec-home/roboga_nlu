from rasa.actions import run_action_server
from rasa_core_sdk.endpoint import *
import os
import rasa_core.run

from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.utils import EndpointConfig
from rasa_core.channels.console import CmdlineInput
import yaml

logger = logging.getLogger(__name__)
directory = os.path.dirname(os.path.realpath(__file__))

from rasa_core.channels import InputChannel
from rasa_core.channels.channel import CollectingOutputChannel, UserMessage, RestInput

from flask import Blueprint, request, jsonify

class SimpleWebBot(InputChannel):

	@classmethod
	def name(cls):
		return "custom_webhook"

	def blueprint(self, on_new_message):
		custom_webhook = Blueprint('custom_webhook', __name__)

		@custom_webhook.route("/", methods=['GET'])
		def health():
			return jsonify({"status": "ok"})

		@custom_webhook.route("/webhook", methods=['POST'])
		def receive():
			payload = request.json
			sender_id = payload.get("sender", None)
			text = payload.get("message", None)
			print(text)
			out = CollectingOutputChannel()
			on_new_message(UserMessage(text, out, sender_id))
			responses = [m for _, m in out.messages]
			return jsonify(responses)

		return custom_webhook

def run_core():
	endpoints = yaml.load(open(directory+"/endpoints.yml").read())
	action_endpoint_url = endpoints['action_endpoint']['url']
	action_endpoint = EndpointConfig(url=action_endpoint_url)
	
	nlu_interpreter = RasaNLUInterpreter(directory+"/models/nlu")
	agent = Agent.load(directory+"/models/core", interpreter = nlu_interpreter, action_endpoint = action_endpoint)
	
	#input_channel = SimpleWebBot()
	#input_channel = HttpInputChannel(5004,"/",RasaChatInput(urlparse.urljoin("http://localhost/","api")))
	input_channel = RestInput()
	
	agent.handle_channels([input_channel], 5004, serve_forever=True)
	

def run_core_basic():
    print("Starting rasa core...")
    cmd = "python -m rasa_core.run --nlu {} --core {} --endpoints {}".format(directory+"/models/nlu", directory+"/models/core", directory+"/endpoints.yml")
    os.system(cmd)

if __name__ == "__main__":
    #run action server as thread
    import threading
    t1 = threading.Thread(target=run_action_server)
    t1.setDaemon(True)
    t1.start()
    #run core
    run_core()