import pytest
from your_module import ArabicPhonemizer  # Replace with the actual import path

@pytest.fixture
def phonemizer():
    return ArabicPhonemizer()

# Test _char_to_phoneme method
def test_char_to_phoneme_known_chars(phonemizer):
    assert phonemizer._char_to_phoneme(u'\u0628') == 'b'
    assert phonemizer._char_to_phoneme(u'\u064A') == 'y'
    assert phonemizer._char_to_phoneme(u'\u0627') == 'A'

def test_char_to_phoneme_unknown_char(phonemizer):
    assert phonemizer._char_to_phoneme('X') == 'X'

# Test _remove_diacritics method
def test_remove_diacritics(phonemizer):
    text = "هَذَا النَصُ مُشَكَلٌ"
    expected = "هذا النص مشكل"
    assert phonemizer._remove_diacritics(text) == expected

def test_remove_diacritics_no_diacritics(phonemizer):
    text = u"السلام عليكم"
    assert phonemizer._remove_diacritics(text) == text

# Test handle_special_cases method
def test_handle_alf_lam_shamsi(phonemizer):
    text = u"الشمس"
    expected = u"اشّمس"
    assert phonemizer.handle_special_cases(text) == expected

def test_handle_alf_lam_qamari(phonemizer):
    text = u"القرآن"
    expected = u"القرآن"
    assert phonemizer.handle_special_cases(text) == expected

def test_handle_alf_lam_with_diacritics(phonemizer):
    text = u"َالْقَمَر"
    assert phonemizer.handle_special_cases(text) == text

def test_handle_alf_lam_multiple_words(phonemizer):
    text = u"الشمس والقمر"
    expected = u"اشّمس والقمر"
    assert phonemizer.handle_special_cases(text) == expected

def test_phonemize_non_arabic_chars(phonemizer):
    text = u"Hello 你好"
    expected = "Hello 你好"
    assert phonemizer.phonemize(text) == expected

def test_phonemize_empty_string(phonemizer):
    text = ""
    expected = ""
    assert phonemizer.phonemize(text) == expected