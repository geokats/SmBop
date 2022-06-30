import json
import argparse

parser = argparse.ArgumentParser(description='Count examples in json file')
parser.add_argument('-f1', type=str, help='the json file')
parser.add_argument('-f2', type=str, help='the json file')
parser.add_argument('-o', type=str, help='the json file')

args = parser.parse_args()

examples = []

with open(args.f1, 'r') as f:
	examples.extend(json.load(f))

with open(args.f2, 'r') as f:
	examples.extend(json.load(f))

with open(args.o, 'w') as f:
	json.dump(examples, f, indent=2)

