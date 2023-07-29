from datasets import load_dataset
import streamlit as st
import random 

def get_idx():
    finished_indices = open('finished_indices.txt', 'r').read().strip()
    if len(st.session_state.examples) > 0:
      prev_index = st.session_state.examples[0][0:1]
    else:
       prev_index = []
    finished_indices = set([int(ind) for ind in finished_indices.split(' ') if len(ind) > 0])
    all_indices = set(range(len(english_data['train'])))
    rem_indices = all_indices - finished_indices - set(prev_index)
    st.write(rem_indices)
    idx = random.choice(list(rem_indices))
    return idx

@st.experimental_singleton
def get_data(): 
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
  english_data['train'] = english_data['train'].select(range(5))
  return english_data, arabic_data

if 'idx' not in st.session_state:
	st.session_state.idx = 0

if 'examples' not in st.session_state:
	st.session_state.examples = []

st.header('Arabic Alpaca Annotation Tool')        
english_data, arabic_data = get_data()

col1, col2 = st.columns(2)
col_btn1, col_btn2 = st.columns(2)

st.markdown("""
<style>
input {
  direction: RTL;
}
</style>
    """, unsafe_allow_html=True)


# with col_btn1:
#     if st.button('skip'):
#         del st.session_state.idx[-2]
#         print(st.session_state.idx)

idx = get_idx()
example = english_data['train'][idx]

# with col2:
with st.form("my_form"):
  st.header("Arabic")
  st.write('**Instruction**')
  inst = st.text_input('Instruction', example['instruction'], label_visibility="collapsed")
  st.write('**Input**')
  inp = st.text_input('Input', example['input'], label_visibility="collapsed")
  st.write('**Output**')
  out = st.text_input('Output', example['output'], label_visibility="collapsed") 

  if st.form_submit_button("Submit"):
    # st.write(st.session_state.examples)
    open('dataset.csv', 'a').write('\n'+ ','.join([inst, inp, out]))
    # open('finished_indices.txt', 'a').write(' '+str(st.session_state.idx))
    st.experimental_rerun()



# with col1:
#     st.header("English")
#     st.write('**Instruction**')
#     st.write(example['instruction_en'])
#     st.write('**Input**')
#     st.write(example['input_en'])
#     st.write('**Output**')
#     st.write(example['output_en'])


