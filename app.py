from flask import Flask, render_template, redirect, url_for
from flask import request, jsonify
from datasets import load_dataset
import random 
import json 
import os 

app = Flask(__name__)

def load_data():
    alpaca_arabic = load_dataset('arbml/alpaca_arabic')
    new_column = list(range(len(alpaca_arabic['train'])))
    alpaca_arabic['train'] = alpaca_arabic['train'].add_column("index", new_column)

    def filter_english(example):
        alphabets = 'abcdefghijklmnopqrstuvwxyz'
        for alph in alphabets:
            if alph in example['instruction']+example['input']+example['output']:
                return True
        return False

    english_data = alpaca_arabic.filter(filter_english)
    all_indices = set([sample['index'] for sample in english_data['train']])

    return all_indices, alpaca_arabic

def save_json(entry):
    data = {}
    if os.path.exists('static/data/dataset.json'):
        with open('static/data/dataset.json') as f:
            data = json.load(f)

        data.update(entry)
    else:
        data = entry

    with open('static/data/dataset.json', 'w') as f:
        json.dump(data, f, ensure_ascii = False, indent=2)

all_indices, alpaca_arabic = load_data()


@app.route('/api/submit',methods = ['POST', 'GET'])
def submit():
    if request.method == 'POST':
        element = {k:request.form[k] for k in request.form}
        idx = element['idx'].split(':')[1].strip()
        save_json({idx: element})
        open('static/data/finished_indices.txt', 'a').write(' '+str(idx))
    return redirect(url_for('index'))
   
@app.route('/api/data')
def send_data():
    if os.path.exists('static/data/finished_indices.txt'):
        finished_indices = open('static/data/finished_indices.txt', 'r').read().strip()
        finished_indices = set([int(ind) for ind in finished_indices.split(' ') if len(ind) > 0])
    else:
        finished_indices = set()

    rem_indices = all_indices - finished_indices
    idx = random.choice(list(rem_indices))
    element = alpaca_arabic['train'][idx]
    element['num_rem'] = len(rem_indices)
    return jsonify(element)

@app.route('/')
def index():
    return render_template('index.html')