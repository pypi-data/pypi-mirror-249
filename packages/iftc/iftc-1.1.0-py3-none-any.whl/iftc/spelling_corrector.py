from iftc.spell_checker.intentional import Intentional
from iftc.spell_checker.unintentional import Unintentional
from iftc.spell_checker.text_processor import remove_mask, text_normalize

class SpellingCorrector:
    def __init__(self):
        self.it_corrector = Intentional()
        self.uit_corrector = Unintentional()

    def acronym_correction(self, text: str):
        text = text_normalize(text)
        corrected_acronym = self.it_corrector.spelling_correction(text)

        return remove_mask(corrected_acronym)

    def telex_correction(self, text: str):
        pass
        # text = text_normalize(text)
        # acronym_corrected = self.it_corrector.spelling_correction(text)
        # sent_corrected   = self.uit_corrector.select_candidate(acronym_corrected)
        # return sent_corrected

    def detect_spelling_error(self, text: str):
        text = text_normalize(text)
        acronym_corrected = self.it_corrector.spelling_correction(text)
        sent_candidates, word_candidates = self.uit_corrector.gen_candidate.sentence_candidate(acronym_corrected)
        return text, word_candidates, sent_candidates