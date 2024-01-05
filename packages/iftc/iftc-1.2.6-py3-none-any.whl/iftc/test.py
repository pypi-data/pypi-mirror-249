
from iftc.spelling_corrector import SpellingCorrector

corrector = SpellingCorrector()

corrected_text = corrector.detect_spelling_error('b ơi, món này giá bn thế')
print(corrected_text)
