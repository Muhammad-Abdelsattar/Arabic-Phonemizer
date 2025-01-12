# Arabic Buckwalter Phonemizer
**A simple Arabic phonemizer to be used for neural TTS systems.**
**Check out this [project](https://github.com/Muhammad-Abdelsattar/Arabic-TTS) for more details.**

## Installation

```bash
pip install arabic_phonemizer
```

## Usage
```python
from arabic_phonemizer import AraabicPhonemizer

phonemizer = AraabicPhonemizer()

phonemizer.phonemize("السَلَامُ عَلَيْكُمُ")
```
output:
```
As~alaAmu Ealayokumu
```

