import os
from aipg.ai_request import LetterMaker
from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)


def trunc_line(line, length:int=30, head:int=15, tail:int=15):
    if len(line) > length:
        bline = line[:head]
        eline = line[-tail:]
        line = f"{bline} ... {eline}"
    return line

def trunc_input(input):
    input = input.split("\n")
    output = ""
    for idx, line in enumerate(input):
        if idx < 3 or idx > len(input) - 4:
            output += f"{trunc_line(line)}<br>"
        if idx == 3:
            output += "...<br>"
    return output

def update_config(l_maker:LetterMaker, new_config:dict):
    name = new_config.pop("name")
    print(f"Update_config func: saving {name}")
    updaters = [l_maker.set_sysmsg, l_maker.set_instructions, l_maker.set_first_message,
                l_maker.set_personal_info, l_maker.set_letter_template]
    print("starting update loop...")
    for input, func in zip(new_config.values(), updaters):
        func(input)
    print("finished loop, entering save_config()")
    return l_maker.save_config(name)
    
    
@app.route('/save_config', methods=['POST'])
def save_config():

    maker = LetterMaker("./job_data.json", config_path="./config.json", config_name="default")

    context = {
        "name": request.form['name'],
        "system_message": request.form['system_message'],
        "instructions": request.form['instructions'],
        "first_message": request.form['first_message'],
        "pinfo": request.form['pinfo'],
        "template": request.form['template']
        }
    new_config = context
    update_config(maker, new_config)

    return render_template('index.html', **context)


@app.route('/', methods=['GET', 'POST'])
def index():        
     
    maker = LetterMaker("./job_data.json", config_path="./config.txt", config_name="default")
    if not maker:
        return render_template('noMaker.html')

    context = {
        "name": f"{maker.config['name']}",
        "system_message": f"{maker.config['system_message']}",
        "instructions": f"{maker.config['instructions']}",
        "first_message": f"{maker.config['first_message']}",
        "pinfo": f"{maker.config['pinfo']}",
        "template": f"{maker.config['template']}"
    }
   

    if request.method == 'POST':
        if 'get_letter' in request.form:
            # Get the form data
            job_data = {
            	"company": request.form['company'],
            	"position": request.form['position'],
            	"description": request.form['description']
            }
            # job_query = f"Company: {company}\nPosition Title: {position}\ndescription: {description}"

            response = maker.get_letter([job_data])
            # Send a request to the external server
            # Display the response on the page
            if response['choices']:
                return render_template('index.html', response=response['choices'][0]['message']['content'], **context)
            if response['status']:
                return render_template('index.html', response=response['response'], **context)
            else:
                return render_template('index.html', response="Something went wrong", **context)
    
    # Render the initial page with the form
    return render_template('index.html', **context)

if __name__ == '__main__':
    app.run()

