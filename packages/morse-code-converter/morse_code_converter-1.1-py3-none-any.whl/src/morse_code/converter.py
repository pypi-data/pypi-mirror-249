# morse_code/converter.py

import pygame
from src.morse_code.constants import DOT_SOUND_FILE, DASH_SOUND_FILE

MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ".": ".-.-.-",
    ",": "--..--",
    "?": "..--..",
    "'": ".----.",
    "!": "-.-.--",
    "/": "-..-.",
    "(": "-.--.",
    ")": "-.--.-",
    "&": ".-...",
    ":": "---...",
    ";": "-.-.-.",
    "=": "-...-",
    "+": ".-.-.",
    "-": "-....-",
    "_": "..--.-",
    '"': ".-..-.",
    "$": "...-..-",
    "@": ".--.-.",
}


def text_to_morse(text):
    morse_code = ""
    for char in text.upper():
        if char == " ":
            morse_code += " "
        else:
            morse_code += MORSE_CODE_DICT[char] + " "
    return morse_code.strip()


def morse_to_text(morse_code):
    morse_code = morse_code.strip().split(" ")
    text = ""
    for code in morse_code:
        for key, value in MORSE_CODE_DICT.items():
            if code == value:
                text += key
    return text.strip()


def play_sound(file_path):
    pygame.mixer.Sound(file_path).play()


def play_morse_code(morse_code):
    pygame.init()
    pygame.mixer.init()

    dot_duration = 300  # Duration of a dot in milliseconds
    dash_duration = 4 * dot_duration  # Duration of a dash
    space_duration = dot_duration  # Duration of space between words

    sound_speed = 20  # Speed of Morse code playback

    for symbol in morse_code:
        if symbol == ".":
            play_sound(DOT_SOUND_FILE)
            pygame.time.wait(int(dot_duration / sound_speed))
        elif symbol == "-":
            play_sound(DASH_SOUND_FILE)
            pygame.time.wait(int(dash_duration / sound_speed))
        elif symbol == " ":
            pygame.time.wait(int(space_duration / sound_speed))

        # Wait until the current sound finishes playing
        while pygame.mixer.get_busy():
            pygame.time.delay(10)

    pygame.mixer.quit()
