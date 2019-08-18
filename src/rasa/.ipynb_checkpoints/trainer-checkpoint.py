from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.training_data import load_data
import os

directory = os.path.dirname(os.path.realpath(__file__))

def train():
	training_data = load_data(directory+"/data/train.md")
	trainer = Trainer(config.load(directory+"/nlu_config.yml"))
	trainer.train(training_data)
	trainer.persist(directory+"/models/current", fixed_model_name="nlu")
	
if __name__ == "__main__":
	train()