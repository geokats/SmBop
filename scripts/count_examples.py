import json
import argparse

parser = argparse.ArgumentParser(description='Count examples in json file')
parser.add_argument('file_path', type=str, help='the json file')

args = parser.parse_args()

with open(args.file_path, 'r') as f:
	examples = json.load(f)
	print(len(examples))