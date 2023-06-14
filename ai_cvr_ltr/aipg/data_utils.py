import csv
import json
import logging
import os
import pprint as pp
import tiktoken
pp.PrettyPrinter(indent=4, depth=5, width=100)




encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
logging.basicConfig(level=logging.INFO)

def make_config(config_path, personal_info, template):

    with open(config_path, "r") as file:
        config = json.load(file)

    p_info = os.path.abspath(personal_info)
    ltr_template = os.path.abspath(template)

    config['configs'][0]['pinfo'] = p_info
    config['configs'][0]['template'] = ltr_template
    tokens = []
    for k, v in config['configs'][0].items():
        if isinstance(v, str):
            # logging.debug(f"(k, tokens(v)):\n{(k, len(encoding.encode(v)))}")
            tokens.append(len(encoding.encode(v)))
        else:
            continue
    # logging.info(f"tokens: {tokens}")
    config['configs'][0]['token_count'] = sum(tokens) 
    with open(config_path, "w") as cfile:
        json.dump(config, cfile, indent=2)
     
def conv_csv(file_path):
    with open(file_path, 'r') as file:
        data = list(csv.DictReader(file, delimiter=','))
    for row in data:
        row["additional_info"] = ""
    
    for idx, row in enumerate(data):
        for k, v in row.items():
            data[idx][k] = v.strip()
    return data        

conv_csv("./data/job_info.csv")

    
