# tests/test_converter.py

from src.morse_code.converter import text_to_morse, morse_to_text


def test_text_to_morse():
    assert text_to_morse("HelloWorld") == ".... . .-.. .-.. --- .-- --- .-. .-.. -.."
    assert text_to_morse("123") == ".---- ..--- ...--"


def test_morse_to_text():
    assert morse_to_text(".... . .-.. .-.. --- .-- --- .-. .-.. -..") == "HELLOWORLD"
    assert morse_to_text(".---- ..--- ...--") == "123"
