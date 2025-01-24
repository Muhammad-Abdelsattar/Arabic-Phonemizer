import os
from pathlib import Path
import re
from .api import EspeakAPI

class EspeakPhonemizer:
    """A phonemizer using the espeak-ng library"""
   
    def __init__(self,
                 library_path:str = "./lib/libespeak-ng.so",
                 voice:str = "ar",
                 use_stress:bool = True,
                 preserved_punctuations:str = ".,?;،:؟!؛",):

        self._init_env(data_path=str(Path(__file__).parent/"espeak-ng-data"))
        self._api = EspeakAPI(library_path)
        
        self.voice = voice
        if self.voice != "ar":
            self._api.set_voice_by_name(self.voice.encode("utf-8"))
        self.use_stress = use_stress
        self.preserved_punctuations = preserved_punctuations

        self.stress_re = re.compile(r"[ˈˌ'-]+")
        self.whitespace_re = re.compile(r"\s+")
        self.punc_re = re.compile(f"([{self.preserved_punctuations}]+)")

    def _init_env(self,
                  data_path:str):
        """
        Initializes the environment by setting the data path for espeak-ng.
        """
        os.environ["ESPEAK_DATA_PATH"] = str(data_path)

    def phonemize(self,
                  text: str) -> str:
        """
        Generates phonemes for the given text.
        args:
            text (str): The text to phonemize.
        returns:
            str: The phonemized text.
        """
        phonemized = []
        text_segments = self.punc_re.split(text)
        for text_segment in text_segments:
            phonemized_segment = self._api.text_to_phonemes(text_segment)
            phonemized_segment = self._process_stress(phonemized_segment)

            if phonemized_segment:
                phonemized.append(phonemized_segment)
            else:
                phonemized.append(text_segment)
        return self._collapse_whitespace("".join(phonemized))

    def _collapse_whitespace(self, 
                             text:str) -> str:
        return self.whitespace_re.sub(" ", text)

    def _process_stress(self, 
                        text:str) -> str:
        if not self.use_stress:
            return self.stress_re.sub("", text)
        return text
