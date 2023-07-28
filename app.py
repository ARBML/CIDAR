from datasets import load_dataset
import streamlit as st
import random 

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
  return english_data, arabic_data

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

def get_idx():
    idx = random.randint(0, len(english_data['train']) - 1)
    return idx

example = english_data['train'][0]



with col_btn1:
    if st.button('skip'):
        idx = get_idx()
        example = english_data['train'][idx]

with col_btn2:
    st.button('submit')

with col2:
    st.header("Arabic")
    st.write('**Instruction**')
    st.text_input('Instruction', example['instruction'], label_visibility="collapsed")
    st.write('**Input**')
    st.text_input('Input', example['input'], label_visibility="collapsed")
    st.write('**Output**')
    st.text_input('Output', example['output'], label_visibility="collapsed")

with col1:
    st.header("English")
    st.write('**Instruction**')
    st.write( example['instruction_en'])
    st.write('**Input**')
    st.write(example['input_en'])
    st.write('**Output**')
    st.write(example['output_en'])


