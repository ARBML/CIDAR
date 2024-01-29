# 🌴CIDAR
*Culturally-Relevant Instruction Dataset For Arabic*
<p align="center">
<img src="https://cdn-uploads.huggingface.co/production/uploads/655e10b1c38270696b290f20/lKec96otC8VdM09SnPKL8.png" width = "150px"/>
</p>

CIDAR contains **10,000** `instructions` and their `output`. The dataset was created by selecting around **9.2k** samples from [Alpagasus](https://huggingface.co/datasets/mlabonne/alpagasus) dataset then translating it to `Arabic` using ChatGPT. In addition, we append that with around **800** Arabic grammar instructions from the webiste [Ask the teacher](https://learning.aljazeera.net/ar/asktheteacher). All the 10,000 samples were reviewed by around 12 reviewers. 


<p align="center">
<img src="./imgs/CIDAR Workflow.png" width = "1200px"/>
</p>

## 📝 CIDAR Annotation

Our data annotation paltform was built on top of flask library. You can follow the next steps to run the app. 

### ⚡️To Run The App:
1. Install the requirements `pip install -r requirements.txt`.
2. Run the app using flask `flask --app app run `.

### ✨ Demo

The annotation app contains two sections: `English` and `Arabic`. Reviewers can make changes on `Instruction`, `Input`, and `Output` to fix mistakes and align data with Arabic culture.

`instruction(str)`: Required instruction.

`input(str)`: [Optional] input for the instruction. For example, when the instruction is find the mistake in the next sentence, the input is the sentence.

`output(str)`: Response for the given instruction.

 Also, reviewers are able to track their contribution record and the number of instructions remaining.
<p align="center">
<img src="imgs/annot-ss.png" width="700"/>
</p>

## 📁 Loading The Dataset
You can download the dataset from [HuggingFace - CIDAR](https://huggingface.co/datasets/arbml/CIDAR). 

```python
from datasets import load_dataset
cidar = load_dataset('arbml/CIDAR-V2')
```

## 📄 Sample From The Dataset:
This sample shows an Arabic-specific intruction which related to `البلاغة(rhetoric)` and `الإعراب(grammatical status)`. The sentence is orignally in Arabic.

 **index**: 10030

 **instruction**: لو سمحت اين صيغة المبالغة في " الجاحظ اديب سيارة اراؤه" و ما اعراب الجملة؟

 **output**:
 
           'صيغة المبالغة في هذه الجملة هي "سيّارة"، فاسم الفاعل من "السير" هو '
           '"سائر/ سائرة" وإذا أردت الدلالة على المبالغة في سير الآراء (أي '
           'شهرتها وكثرة تداولها) قلت "آراء سيّارة".\r\n'
           'أما إعراب الجملة فهو: "الجاحظُ": مبتدأ مرفوع بالضمة. "أديبٌ": خبر '
           'مرفوع بالضمة. "سيارةٌ": خبر متقدم، و"آراؤُه": مبتدأ متأخر، وهو '
           'مضاف والهاء ضمير متصل مضاف إليه في محل جر.  ويمكن اعتبار "سيارة" '
           'مبتدأ وهو وصف يعمل عمل فعله، و"آراؤُه" فاعل سدّ مسدّ الخبر.\r\n'
           'وفي الحالتين فجملة "سيارة آراؤه" جملة اسمية في محل رفع نعت '
           'لـ"أديب".'

## 📉 Statistics

...

## 🧩 Contributers
There were at least 12 contributors to the annotation of CIDAR. You can check the list [here](https://alpacaarabic-production.up.railway.app/explore).

## ⛔️ Limitations and Future Work
CIDAR is intended for **research** purposes only. The authors disclaim any responsibility for misuse and condemn any use contrary to **Arabic culture** or **Islamic values**. Even though subjected to human verification, there is no guarantee that responses are entirely aligned with Arabic culture and Islamic values. Users of the dataset are urged to exercise caution, employ critical thinking, and seek guidance from representative figures when necessary.

## 🔑 License
CIDAR is intended and licensed for **research** use only. The dataset and weight diffs are licensed uder **CC BY NC 4.0** (LIMITED TO NON-COMMERCIAL USE). Models trained using the dataset should not be used outside of research purposes.
[Creative Commons NonCommercial (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/deed.en).
