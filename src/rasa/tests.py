import unittest
import pandas
from rasa_nlu.model import Interpreter
from rasa_nlu.training_data import load_data
from rasa.trainer import main
import os
import json

directory = os.path.dirname(os.path.realpath(__file__))

def hasSlot(slot, nlu_result):
	present = False
	for entity in nlu_result['entities']:
		if(entity['value'] == slot or entity['entity'] == slot):
			present = True
	return present

#Run the tests on the base_test.md file nlu model and print the cases where it fails
class NLUTestCase(unittest.TestCase):
	def setUp(self):
		self.interpreter = Interpreter.load(directory+"/models/nlu/")
		self.tests = load_data(directory+"/data/base_test.md")
		self.verificationErrors = []

	def test_nlu(self):
		for test in self.tests.intent_examples:
			result = self.interpreter.parse(test.text)
			message = "\nText: {}\n    Intent found: {} / Intent target: {}".format(test.text, result['intent']['name'], test.get('intent'))
			try: self.assertEqual(result['intent']['name'], test.get('intent'), message)
			except AssertionError as e: self.verificationErrors.append(str(e))
			if(test.get('entities')):
				for slot in test.get('entities'):
					message = "\nText: {}\n    Slot target: {}\n    Slots found:\n         {}".format(test.text, slot['value'], json.dumps(result['entities'], indent=2))
					try: self.assertTrue(hasSlot(slot['value'], result), message)
					except AssertionError as e: self.verificationErrors.append(str(e))
		for error in self.verificationErrors:
			print(error)
		print("Numero de erros: ", len(self.verificationErrors))
					
def main(train_arg=False):
	if(train_arg):
		main(nlu = True, core = True)
	suite = unittest.TestLoader().loadTestsFromTestCase(NLUTestCase)
	unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--train", help="train the nlu and the core", action="store_true")
	args = parser.parse_args()
	main(train_arg=args.train)
