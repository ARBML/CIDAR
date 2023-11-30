# CIDAR
<center>
<img src="https://cdn-uploads.huggingface.co/production/uploads/655e10b1c38270696b290f20/lKec96otC8VdM09SnPKL8.png" width = "150px"/>
</center>
CIDAR: Culturally-Relevant Instruction Dataset For Arabic. CIDAR contains 10,000 instructions and their outputs. The dataset was created by selecting around 9.2k samples from [Alpagasus](https://huggingface.co/datasets/mlabonne/alpagasus) dataset then translating it using ChatGPT. In addition to that we append that with around 800 instructions from the webiste [Ask the teacher](https://learning.aljazeera.net/ar/asktheteacher). All the 10,000 samples are reviewed by around 10 reviewers. 

## CIDAR Annotation
First install the requirements `pip install -r requirements.txt` then run the app using flask `flask --app app run `.

<center>
<img src="imgs/annot-ss.png"/>
</center>

## Loading the dataset
You can download the dataset from HuggingFace. 

```python
from datasets import load_dataset
cidar = load_dataset('arbml/CIDAR')
```