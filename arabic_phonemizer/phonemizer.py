import platform
from .espeak import EspeakPhonemizer
from .constants import *
from pathlib import Path

class ArabicPhonemizer:
    def __init__(self,
                 phonemizer_type:str = "espeak",
                 separator:str = ""):

        self.phonemizer_type = phonemizer_type
        if self.phonemizer_type == "espeak":
            system = platform.system().lower()
            architecture = platform.machine().lower()
            if system == "linux":
                library_name = "libespeak-ng.so"
            elif system == "darwin":
                library_name = "libespeak-ng.dylib"
            elif system == "windows":
                library_name = "espeak-ng.dll"
            else:
                raise ValueError(f"Unsupported system: {system}")

            library_path = Path(__file__).parent / "espeak" / "shared_libs" / system / architecture / library_name

            self.phonemizer = EspeakPhonemizer(voice="ar", 
                                               preserved_punctuations=".,?",
                                               use_stress=True,
                                               library_path=library_path)

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
        if self.phonemizer_type=="espeak":
            text = self._handle_ta2_marboota_cases(text)
            phonemized = self.phonemizer.phonemize(text)
            return phonemized
        else:
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
        text = self._handle_special_words(text)
        text = self._handle_alf_wasl_cases(text)
        text = self._handle_ta2_marboota_cases(text)
        text = self._handle_alf_lam_cases(text)
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
            if undiacritized_word[0:4] in ["وبال","فبال","فكال","وكال","وفال","فوال"] and undiacritized_word[4] in SHAMSI_LETTERS+QAMARI_LETTERS:
                index = list_word.index(undiacritized_word[4])
                alf_index = list_word.index("ا")
                for idx, char in enumerate(list_word[alf_index:index]):
                    if char in TASHKEEL:
                        list_word.remove(char)
                list_word.remove("ا")
                lam_index = list_word.index("ل")
                if undiacritized_word[4] in SHAMSI_LETTERS:
                    list_word.remove("ل")
                    if list_word[lam_index] != "ّ": #force Shadda after lam shamsia
                        list_word.insert(lam_index+1,"ّ")
                elif undiacritized_word[4] in QAMARI_LETTERS:
                    list_word.insert(lam_index+1,"ْ")
                    
            elif undiacritized_word[0:3] in ["بال","كال","فال","وال","أال"] and undiacritized_word[3] in SHAMSI_LETTERS+QAMARI_LETTERS:
                index = list_word.index(undiacritized_word[3])
                alf_index = list_word.index("ا")
                for idx, char in enumerate(list_word[alf_index:index]):
                    if char in TASHKEEL:
                        list_word.remove(char)
                list_word.remove("ا")
                lam_index = list_word.index("ل")
                if undiacritized_word[3] in SHAMSI_LETTERS:
                    list_word.remove("ل")
                    if list_word[lam_index] != "ّ": #force Shadda after lam shamsia
                        list_word.insert(lam_index+1,"ّ")
                elif undiacritized_word[3] in QAMARI_LETTERS:
                    list_word.insert(lam_index+1,"ْ")

            elif undiacritized_word[0:2] == "ال" and undiacritized_word[2] in SHAMSI_LETTERS+QAMARI_LETTERS:
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
            elif undiacritized_word[0:2] == "لل" and undiacritized_word[2] in SHAMSI_LETTERS+QAMARI_LETTERS:
                index = list_word.index(undiacritized_word[2])
                lam_index_1 = list_word.index("ل")
                lam_index_2 = list_word.index("ل", lam_index_1+1)
                for idx, char in enumerate(list_word[lam_index_2:index]):
                    if char in TASHKEEL:
                        list_word.remove(char)
                lam_index_1 = list_word.index("ل")
                lam_index_2 = list_word.index("ل", lam_index_1+1)
                if undiacritized_word[2] in SHAMSI_LETTERS:
                    list_word.pop(lam_index_2)
                    if list_word[lam_index_2+1] != "ّ": #force Shadda after lam shamsia
                        list_word.insert(lam_index_2+1,"ّ")
                elif undiacritized_word[2] in QAMARI_LETTERS:
                    list_word.insert(lam_index_2+1,"ْ")
            handled_words.append("".join(list_word))
        return " ".join(handled_words)

    def _handle_alf_wasl_cases(self,
                              text:str) -> str:
        """
        Handles the case of "ا" at the beginning of a word.
        args:
            text (str): The input text.
        returns:
            str: The modified text with the case handled.
        """
        chars_list = list(text)
        matches = alf_wasl_pattern.finditer(text)
        bos_matches = alf_lam_bos.finditer(text)

        for bos_match in bos_matches:
            start = bos_match.start(2)
            end = bos_match.end(2)
            word = list(self._handle_alf_lam_cases(bos_match.group(2)))
            word[0] = "أَ"
            for i in range(start, end):
                chars_list[i] = ""
            chars_list[start] = "".join(word)

        for match in matches:
            idx = match.start()
            if self._starts_with_alf_lam(match.group()): 
                pass
            elif chars_list[idx+1] == "َ":
                chars_list[idx] = "أ"
            elif chars_list[idx+1] == "ُ":
                chars_list[idx] = "أ"
            elif chars_list[idx+1] == "ِ":
                chars_list[idx] = "إ"
            elif chars_list[idx+1] in ARABIC_LETTERS:
                chars_list[idx] = "إِ"
            else:
                pass
        
        return "".join(chars_list)

    def _handle_ta2_marboota_cases(self,
                                   text: str) -> str:
        """
        Handles the case of "ة" at the ending of a word.
        args:
            text (str): The input text.
        returns:
            str: The modified text with the case handled.
        """
        words = text.split()
        chars_list = list(text)
        matches = ta2_marbootah_sakenah_pattern.finditer(text)
        for match in matches:
            if self._starts_with_alf_lam(match.group()):
                chars_list[match.end()-2:match.end()] = "هْ"
            else:
                if sentence_has_words_pattern.match(text[match.end()+1:]):
                    chars_list[match.end()-2:match.end()] = "تْ"
                else:
                    chars_list[match.end()-2:match.end()] = "هْ"
        return "".join(chars_list)
    
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
        handled = list(text)
        matches = special_words_pattern.finditer(text)
        for m in matches:
            start = m.start(2)
            end = m.end(2)
            handled_word = SPECIAL_WORDS_MAP[self._remove_diacritics(m.group(2))]
            for i in range(start, end):
                handled[i] = ""
            handled[start] = handled_word
        return "".join(handled)
            
        # for word in words:
        #     match = segment_pattern.match(word)
        #     undiacritized_word = self._remove_diacritics(match.group(2))
        #     if undiacritized_word in SPECIAL_WORDS_MAP:
        #         handled_words.append(match.group(1)+SPECIAL_WORDS_MAP[undiacritized_word]+match.group(3))
        #     else:
        #         handled_words.append(word)
        # return " ".join(handled_words)

    def _handle_undiacritizable_alf(self,
                                     text:str) -> str:
        """
        Handles the case where the letter "ا" shouldn't be diacritized.
        args:
            text (str): The input text.
        returns:
            str: The modified text with the special case handled.
        """
        word_list = list(text)
        for i in range(len(word_list)):
            if word_list[i] == "ا":
                #Todo
                pass

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
    
    def _starts_with_alf_lam(self,
                             text:str) -> bool:
        """
        Checks if the input text starts with the letter "ال".
        args:
            text (str): The input text.
        returns:
            bool: True if the text starts with "ال", False otherwise.
        """
        patterns = [alf_lam_pattern, char_alf_lam_pattern, char_char_alf_lam_pattern]
        if any(pattern.match(text) for pattern in patterns):
            return True
        return False