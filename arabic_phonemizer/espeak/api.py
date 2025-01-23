from pathlib import Path
from typing import Union, Optional, Tuple
import ctypes
from ctypes import CDLL
from functools import lru_cache
from dataclasses import dataclass

@dataclass
class Voice:
    """Dataclass representing voice properties from espeak-ng."""
    name: str
    languages: str
    identifier: str

class Voice(ctypes.Structure):  # pylint: disable=too-few-public-methods
    """A class to fetch voices information from the espeak library.

    The espeak_VOICE struct is defined in speak_lib.h from the espeak code.
    Here we use only name (voice name), languages (language code) and
    identifier (voice file) information.

    """
    _fields_ = [
        ('name', ctypes.c_char_p),
        ('languages', ctypes.c_char_p),
        ('identifier', ctypes.c_char_p)]

def struct_to_dataclass(struct) -> Voice:
    """Convert a C struct to a Voice dataclass."""
    return Voice(
        name=struct.name.decode() if struct.name else "",
        languages=struct.languages.decode() if struct.languages else "",
        identifier=struct.identifier.decode() if struct.identifier else ""
    )

class EspeakAPI:
    """
    A Singleton wrapper for the espeak-ng library that exposes required text-to-phoneme functionality.
    
    This class implements a thread-safe Singleton pattern as the underlying espeak-ng C code
    uses global variables and is not designed for concurrent usage. The library should NOT
    be used in multithreaded/multiprocess contexts.
    
    Attributes:
        _instance (EspeakAPI): Singleton instance of the class
        _initialized (bool): Flag indicating if the instance has been initialized
        _library_path (Path): Path to the espeak-ng shared library
        _espeak (CDLL): Loaded espeak-ng library instance
    """
    
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of EspeakAPI exists."""
        if cls._instance is None:
            cls._instance = super(EspeakAPI, cls).__new__(cls)
        return cls._instance

    def __init__(self, library_path: Union[str, Path]) -> None:
        """
        Initialize the espeak-ng library (only executed once due to Singleton pattern).
        
        Args:
            library_path: Path to the espeak-ng shared library
            
        Raises:
            RuntimeError: If library loading or initialization fails
        """
        if self._initialized:
            return

        try:
            self._library_path = Path(library_path)
            self._espeak = CDLL(str(self._library_path))
            
            # Initialize espeak with default settings
            if self._espeak.espeak_Initialize(0x0002, 0, None, 0) <= 0:
                raise RuntimeError('Failed to initialize espeak shared library')
            
            self._initialized = True
            
        except OSError as error:
            raise RuntimeError(f'Failed to load espeak library: {error}') from None

        # Set default voice to Arabic
        if self.set_voice_by_name(b"ar") != 0:
            raise RuntimeError('Failed to set default voice to Arabic, Make sure the data files for the voice sem/ar exist in your data path.')

    @property
    def library_path(self) -> Path:
        """Get the path of the loaded library."""
        return self._library_path

    @lru_cache(maxsize=1)
    def info(self) -> Tuple[bytes, bytes]:
        """
        Get version and data path information of the loaded library.
        
        Returns:
            Tuple containing (version, data_path)
        """
        self._espeak.espeak_Info.restype = ctypes.c_char_p
        data_path = ctypes.c_char_p()
        version = self._espeak.espeak_Info(ctypes.byref(data_path))
        return version, data_path.value

    def text_to_phonemes(self, text: str) -> str:
        """
        Convert text to phonemes using espeak-ng.
        
        Args:
            text: Input text to be converted to phonemes
            
        Returns:
            String containing the phonemized text with space-separated phonemes
        """
        text_ptr = ctypes.pointer(ctypes.c_char_p(text.encode('utf8')))
        # No tie is used to separate phonemes
        phonemes_mode = 0x03 | 0x01 << 4
        
        phonemized = []
        while text_ptr.contents.value:
            phoneme = self._text_to_phonemes(text_ptr, phonemes_mode)
            if phoneme:
                phonemized.append(phoneme.decode())
                
        return " ".join(phonemized)

    def set_voice_by_name(self, name: bytes) -> int:
        """
        Set the voice by name.
        
        Args:
            name: Voice name to set (e.g., b"sem/ar" for Arabic)
            
        Returns:
            0 on success, non-zero on failure
        """
        self._espeak.espeak_SetVoiceByName.argtypes = [ctypes.c_char_p]
        return self._espeak.espeak_SetVoiceByName(name)

    def get_current_voice(self) -> Optional[Voice]:
        """
        Get the currently set voice.
        
        Returns:
            Voice dataclass instance or None if no voice is set
        """
        self._espeak.espeak_GetCurrentVoice.restype = ctypes.POINTER(Voice)
        voice_struct = self._espeak.espeak_GetCurrentVoice()
        return struct_to_dataclass(voice_struct.contents) if voice_struct else None

    def _text_to_phonemes(self, text_ptr, phonemes_mode: int) -> Optional[bytes]:
        """
        Internal method to convert text to phonemes using espeak-ng.
        
        Args:
            text_ptr: Pointer to the text to be phonemized
            phonemes_mode: Bit field controlling phoneme output format
            
        Returns:
            Encoded string containing computed phonemes or None
        """
        text_mode = 1  # utf-8 encoding
        
        f_text_to_phonemes = self._espeak.espeak_TextToPhonemes
        f_text_to_phonemes.restype = ctypes.c_char_p
        f_text_to_phonemes.argtypes = [
            ctypes.POINTER(ctypes.c_char_p),
            ctypes.c_int,
            ctypes.c_int
        ]
        return f_text_to_phonemes(text_ptr, text_mode, phonemes_mode)