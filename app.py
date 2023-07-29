from flask import Flask, render_template
from flask import request, jsonify
from datasets import load_dataset
import random 

app = Flask(__name__)

alpaca_arabic = load_dataset('arbml/alpaca_arabic')
new_column = list(range(len(alpaca_arabic['train'])))
alpaca_arabic['train'] = alpaca_arabic['train'].add_column("index", new_column)

def filter_english(example):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    for alph in alphabets:
        if alph in example['instruction']+example['input']+example['output']:
            return True
    return False

def filter_arabic(example):
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    for alph in alphabets:
        if alph in example['instruction']+example['input']+example['output']:
            return False
    return True

english_data = alpaca_arabic.filter(filter_english)
arabic_data = alpaca_arabic.filter(filter_arabic)
english_data['train'] = english_data['train'].select(range(100))
all_indices = set([sample['index'] for sample in english_data['train']])
print(all_indices)
@app.route('/api/submit',methods = ['POST', 'GET'])
def submit():
    if request.method == 'POST':
        inst = request.form['inst']
        inp = request.form['inp']
        out = request.form['out']
        idx = request.form['idx']
        open('dataset.csv', 'a').write('\n'+ ','.join([inst, inp, out]))
        open('finished_indices.txt', 'a').write(' '+str(idx))
    return render_template('index.html')
   
@app.route('/api/data')
def send_data():
    finished_indices = open('finished_indices.txt', 'r').read().strip()
    finished_indices = set([int(ind) for ind in finished_indices.split(' ') if len(ind) > 0])
    rem_indices = all_indices - finished_indices
    idx = random.choice(list(rem_indices))
    return jsonify(alpaca_arabic['train'][idx])

@app.route('/')
def index():
    return render_template('index.html')