# Acrolint

**Acrolint** is a extreamly light weight python library for extraction of acronyms used in your latex and text files, that grow to long to remeber where you used your BUAs (Big Ugly Actonyms)

---

## ✨ Features
- Extracting both the acrronyms and the deffintions for filling in any acronym pages to your work
- Detect any acronyms you did not define all the UDAs
- Track where they are first used sao you can fill in the deffinions or check they are deffomed were thy are firt used in your multi file project
- Suports multiple files
- JSON file output for the ability to store all of your acronyms and to enable down stream anaylysis

---

## 📦 Installation

```bash
pip install acrolint

## 💨 Fast start
from acrolint import acrolint, output_file

files = [
    "chapter1.tex",
    "chapter2.tex",
    "chapter3.tex"
]

result = acrolint(files)

output_file(result, "acronyms.json")