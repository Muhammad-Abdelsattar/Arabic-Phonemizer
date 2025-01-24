# Arabic Phonemizer
**A simple Arabic phonemizer to be used for neural Arabic TTS systems.**
**Check out this [project](https://github.com/Muhammad-Abdelsattar/Arabic-TTS) for more details.**

**It currently supports espeak-ng via precompiled shared libs and ctypes.**
**Why include shared libs in the library?**
**First, installing espeak-ng on windows is a pain in the ass. Second, installing espeak-ng on linux and Mac requires sudo privileges which may not always be available.**

## Installation

```bash
git clone https://github.com/Muhammad-Abdelsattar/Arabic-Phonemizer.git
cd arabic_phonemizer
pip install .
```
**OR**
```bash
pip install git+https://github.com/Muhammad-Abdelsattar/Arabic-Phonemizer.git@master#egg=arabic-phonemizer
```

## Usage
```python
from arabic_phonemizer import AraabicPhonemizer

phonemizer = AraabicPhonemizer()

print(phonemizer.phonemize("السَلَامُ عَلَيْكُمُ"))
```
output:
```
ʔassalˌaːmu ʕˌalaˈikumˌu
```

