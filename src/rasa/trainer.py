from rasa_nlu.model import Trainer
import rasa_nlu.config
import rasa_core.config
from rasa_core.agent import Agent
from rasa_nlu.training_data import load_data
import os

directory = os.path.dirname(os.path.realpath(__file__))

#Train the rasa nlu model
def train_nlu():
	training_data = load_data(directory+"/data/train.md")
	trainer = Trainer(rasa_nlu.config.load(directory+"/nlu_config.yml"))
	trainer.train(training_data)
	trainer.persist(directory, project_name="models" , fixed_model_name="nlu")

#Train the rasa core model
def train_core():
	policies = rasa_core.config.load(directory+"/policy_config.yml")
	agent = Agent(domain = directory+"/domain.yml", policies = policies)
	data = agent.load_data(directory+"/data/stories.md")
	agent.train(data)
	agent.persist(directory+"/models/core")

def main(nlu=False, core=False):
	if(nlu):
		train_nlu()
	if(core):
		train_core()
	
if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--nlu", help="train the nlu", action="store_true")
	parser.add_argument("--core", help="train the nlu", action="store_true")
	args = parser.parse_args()
	main(nlu=args.nlu, core=args.core)