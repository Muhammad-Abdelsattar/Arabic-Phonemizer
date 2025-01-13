from .constants import (ARABIC2BUCKWALTER,
                        SHAMSI_LETTERS,
                        QAMARI_LETTERS,
                        SPECIAL_WORDS_MAP,
                        TASHKEEL)

class ArabicPhonemizer:
    def __init__(self,
                 separator:str = ""):
        self.separator = separator

    def phonemize(self,
                  text: str) -> str:
        """
        Phonemizes a string of text.
        args:
            text (str): The text to be phonemized.
        returns:
            str: A string of phonemes corresponding to the input text.
        """
        text = self.handle_special_cases(text)
        phonemized = ""
        for char in text:
            phonemized += self._char_to_phoneme(char)
            if self.separator:
                phonemized += self.separator
        return phonemized

    def handle_special_cases(self, text: str) -> str:
        """
        Handles special cases in the input text.
        args:
            text (str): The input text.
        returns:
            str: The modified text with special cases handled.
        """
        text = self._handle_alf_lam_cases(text)
        text = self._handle_special_words(text)
        return text

    def _handle_alf_lam_cases(self,
                              text: str) -> str:
        """
        Handles special cases (shamsia or qamaria) related to the letters "ال" in the input text.
        args:
            text (str): The input text.
        returns:
            str: The modified text with special cases handled.
        """
        words = text.split()
        handled_words = []
        for word in words:
            list_word = list(word)
            undiacritized_word = self._remove_diacritics(word)
            if undiacritized_word[0:2] == "ال" and undiacritized_word[2] in SHAMSI_LETTERS+QAMARI_LETTERS:
                index = list_word.index(undiacritized_word[2])
                for idx, char in enumerate(list_word[:index]):
                    if char in TASHKEEL:
                        list_word.remove(char)
                lam_index = list_word.index("ل")
                if undiacritized_word[2] in SHAMSI_LETTERS:
                    list_word.remove("ل")
                    if list_word[lam_index+1] != "ّ": #force Shadda after lam shamsia
                        list_word.insert(lam_index+1,"ّ")
                elif undiacritized_word[2] in QAMARI_LETTERS:
                    list_word.insert(lam_index+1,"ْ")
            handled_words.append("".join(list_word))

        return " ".join(handled_words)
    
    def _handle_special_words(self,
                              text:str) -> str:
        """
        Handles words with special pronounciation. See constants.py for more info.
        args:
            text (str): The input text.
        returns:
            str: The modified text with special cases handled.
        """
        words = text.split()
        handled_words = []
        for word in words:
            undiacritized_word = self._remove_diacritics(word)
            if undiacritized_word in SPECIAL_WORDS_MAP:
                handled_words.append(SPECIAL_WORDS_MAP[undiacritized_word])
            else:
                handled_words.append(word)
        return " ".join(handled_words)

    def _char_to_phoneme(self, char: str) -> str:
        """
        Converts a character to its corresponding phoneme representation.
        args:
            char (str): The character to be converted.
        returns:
            str: The phoneme representation of the character.
        """
        if char in ARABIC2BUCKWALTER:
            return ARABIC2BUCKWALTER[char]
        else:
            return char

    def _remove_diacritics(self,
                           text: str) -> str:
        """
        Removes diacritics from the input text.
        args:
            text (str): The input text.
        returns:
            str: The text with diacritics removed.
        """
        for char in TASHKEEL:
            text = text.replace(char, '')
        return text