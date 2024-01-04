# IFT Correction

IFT Correction(Informal Text Correction) is a library of spelling correction for Vietnamese informal text type(informal text is the type of text as daily communication messages)

## Installation

```
pip install iftc
```

## Example Usage

### Only spelling correction for acronyms

```python
from iftc.spelling_corrector import SpellingCorrector

corrector = SpellingCorrector()

corrected_text = corrector.acronym_correction('b ơi, món này giá bn thế')
print(corrected_text)
```

This should print:

```console
'bạn ơi, món này giá bao nhiêu thế'
```

### Spelling correction for detect spelling error

```python
from iftc.spelling_corrector import SpellingCorrector

corrector = SpellingCorrector()

text, word_candidates = corrector.detect_spelling_error('b ơi, món này giá bn thế')
print(word_candidates)
```
