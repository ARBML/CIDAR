from flask import Flask, render_template, redirect, url_for
from flask import request, jsonify
from datasets import load_dataset
from flask_apscheduler import APScheduler
import random 
import json 
import os
import subprocess

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()

class Config:
    SCHEDULER_API_ENABLED = True

scheduler.init_app(app)

def get_finished_indices():
    if os.path.exists('static/data/dataset.json'):
        with open('static/data/dataset.json') as f:
            data = json.load(f)

        finished_indices = []
        for element in data:
            finished_indices.append(int(element['index']))
        return set(finished_indices)
    else:
        return set()

def load_data():
    alpaca_arabic = load_dataset('arbml/alpaca_arabic')
    # new_column = list(range(len(alpaca_arabic['train'])))
    # alpaca_arabic['train'] = alpaca_arabic['train'].add_column("index", new_column)

    def filter_english(example):
        alphabets = 'abcdefghijklmnopqrstuvwxyz'
        for alph in alphabets:
            if alph in example['instruction']+example['input']:
                return True
        return False

    english_data = alpaca_arabic.filter(filter_english)
    all_indices = set([sample['index'] for sample in english_data['train']])

    return all_indices, alpaca_arabic

def save_json(entry):
    if os.path.exists('static/data/dataset.json'):
        with open('static/data/dataset.json') as f:
            data = json.load(f)
        data.append(entry)

    with open('static/data/dataset.json', 'w') as f:
        json.dump(data, f, ensure_ascii = False, indent=2)

all_indices, alpaca_arabic = load_data()


@app.route('/api/submit',methods = ['POST', 'GET'])
def submit():
    if request.method == 'POST':
        element = {k:request.form[k] for k in request.form}
        save_json(element)
    return redirect(url_for('index'))
   
@app.route('/api/data')
def send_data():
    
    finished_indices = get_finished_indices()
    rem_indices = all_indices - finished_indices
    index = random.choice(list(rem_indices))
    element = alpaca_arabic['train'][index]
    element['num_rem'] = len(rem_indices)
    return jsonify(element)

@app.route('/api/saved')
def send_saved_data():
    element = {
            "instruction":'',
            "input" :'',
            "output" :'',
            "instruction_en":'',
            "input_en" :'',
            "output_en" :'',
            "num_rem":0,
            "index":-1
        }
    with open('static/data/dataset.json') as f:
        data = json.load(f)
    if len(data):
        saved_indices = list(range(len(data)))
        index = random.choice(saved_indices)
        element = data[index]
        element['num_rem'] = len(saved_indices)
    return jsonify(element)

@scheduler.task('interval', id='do_push_hf', hours=1)
def push_hub():
    TOKEN = os.environ.get('HF_TOKEN')
    subprocess.run(["huggingface-cli", "login", "--token", TOKEN])
    with open('static/data/dataset.json') as f:
        data = json.load(f)
    
    if len(data):
        dataset = load_dataset("json", data_files="static/data/dataset.json",  download_mode = "force_redownload")
        dataset.push_to_hub('arbml/alpaca_arabic_v3')

def init_dataset():
    os.makedirs('static/data', exist_ok=True)
    try:
        print('loading previous dataset')
        dataset = load_dataset('arbml/alpaca_arabic_v3', download_mode = "force_redownload", verification_mode='no_checks')
        print(dataset)
        data = [elm for elm in dataset['train']]
    except:
        data = []

    with open('static/data/dataset.json', 'w') as f:
        json.dump(data, f, ensure_ascii = False, indent=2)
    
@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/')
def index():
    return render_template('index.html')

init_dataset()
scheduler.start()

if __name__ == '__main__':
    app.run(port=5000)
