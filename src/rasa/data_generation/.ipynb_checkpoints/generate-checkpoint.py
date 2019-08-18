import os
from chatette.facade import Facade
from rasa_nlu.training_data import load_data

directory = os.path.dirname(os.path.realpath(__file__))
directory_up = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

def converter(file):
	input_training_file = directory+'/output/train/'
	data = load_data(input_training_file)
	output_md_file = directory_up+'/rasa/data/'+file
	with open(output_md_file,'w') as f:
		f.write(data.as_markdown())

def generate(file):
	facade = Facade.get_or_create(directory+'/'+file, directory+'/output', adapter_str="rasa")
	facade.run()
	
def main(test=False):
	if(not test):
		input_file = 'master.chatette'
		output_file = 'train.md'
	else:
		input_file = 'test.chatette'
		output_file = 'base_test.md'
	generate(input_file)
	converter(output_file)

if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("--test", help="generate the test files", action="store_true")
	args = parser.parse_args()
	main(test=args.test)