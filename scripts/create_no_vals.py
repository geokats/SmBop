import json
import argparse

CLAUSE_KEYWORDS = ('select', 'from', 'where', 'group', 'order', 'limit', 'intersect', 'union', 'except')
JOIN_KEYWORDS = ('join', 'on', 'as')
WHERE_OPS = ('not', 'between', '=', '>', '<', '>=', '<=', '!=', 'in', 'like', 'is', 'exists')
UNIT_OPS = ('none', '-', '+', "*", '/')
AGG_OPS = ('none', 'max', 'min', 'count', 'sum', 'avg')
COND_OPS = ('and', 'or')
SQL_OPS = ('intersect', 'union', 'except')
ORDER_OPS = ('desc', 'asc')
DISTINCT = ('distinct',)
BY = ('by',)

sql_words = CLAUSE_KEYWORDS + JOIN_KEYWORDS + WHERE_OPS + \
    UNIT_OPS + AGG_OPS + COND_OPS + SQL_OPS + ORDER_OPS + DISTINCT + BY
sql_words = set(sql_words).union(set([word.upper() for word in sql_words]))

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, help='the input json file')
parser.add_argument('-t', type=str, help='the input json tables file')
parser.add_argument('-o', type=str, help='the output json file')

args = parser.parse_args()

def is_value(tok, column_names, table_names, aliases):
    tok = tok.lower()

    if tok in ['(', ')', '.', ',', '*', ';']:
        return False
    if tok in sql_words:
        return False
    if tok in table_names:
        return False
    if tok in aliases:
        return False
    if tok in column_names:
        return False
    if "." in tok:
        # If there is a dot in the name
        try:
            table, column = tok.split(".")
            if (table in table_names or table in aliases) and column in column_names:
                return False
        except:
            #If there are more than one dots, it's not a column name
            print(tok)
    
    return True



with open(args.i, 'r') as f:
    examples = json.load(f)

tables = {}
with open(args.t, 'r') as f:
    tables_raw = json.load(f)

for table in tables_raw:
    db_id = table['db_id']
    column_names = [name.lower() for i, name in table['column_names_original']]
    table_names = [name.lower() for name in table['table_names_original']]
    tables[db_id] = {
        'column_names': column_names,
        'table_names': table_names
    }


for example in examples:
    if 'query_toks_no_value' in example:
        continue

    aliases = [example['query_toks'][i+1].lower() for i, tok in enumerate(example['query_toks']) if tok in ('as', 'AS', 'As')]

    example['query_toks_no_value'] = []
    for tok in example['query_toks']:
        if tok in ['\'', '\"']:
            continue
        elif is_value(tok, tables[example['db_id']]['column_names'], tables[example['db_id']]['table_names'], aliases):
            example['query_toks_no_value'].append('value')
        else:
            example['query_toks_no_value'].append(tok)

with open(args.o, 'w') as f:
    json.dump(examples, f, indent=2)
