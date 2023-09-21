import json
import argparse

parser = argparse.ArgumentParser(description='Count examples in json file')
parser.add_argument('-i', type=str, help='the json file')
parser.add_argument('-o', type=str, help='the json file')

args = parser.parse_args()

with open(args.i, 'r') as f:
	examples = json.load(f)

with open(args.o, 'w') as f:
	for example in examples:
		query = ' '.join(example['query'].split())
		db_id = example['db_id']
		f.write(f"{example}\t{db_id}\n")
