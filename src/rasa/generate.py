import os
from chatette.facade import Facade
from rasa_nlu.training_data import load_data

directory = os.path.dirname(os.path.realpath(__file__))
directory_chatette = directory + '/data_generation'

#Generate .json training format from the .chatette files
def generate(file):
	facade = Facade.get_or_create(directory_chatette+'/'+file, directory_chatette+'/output', adapter_str="rasa")
	facade.run()

#Converter of .json training format to .md
def converter(file):
	input_training_file = directory_chatette+'/output/train/'
	data = load_data(input_training_file)
	output_md_file = directory+'/data/'+file
	with open(output_md_file,'w') as f:
		f.write(data.as_markdown())

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
