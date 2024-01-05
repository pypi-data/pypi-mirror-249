# morse_code/minion_mode.py

import argparse
from colorama import Fore, Style

from src.morse_code.converter import text_to_morse, morse_to_text, play_morse_code


def print_colored(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{text}{Style.RESET_ALL}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert text to Morse code and play it in Minion style."
    )
    parser.add_argument("--encrypt", "-e", help="Encrypt a message to Morse code")
    parser.add_argument("--decrypt", "-d", help="Decrypt Morse code to a message")
    parser.add_argument(
        "--play", "-p", action="store_true", help="Play the Morse code as sound"
    )

    args = parser.parse_args()

    if args.encrypt:
        text_to_encrypt = args.encrypt
        morse_code = text_to_morse(text_to_encrypt)
        print_colored(
            f"Message to Encrypt: {text_to_encrypt}",
            color=Fore.GREEN,
            style=Style.BRIGHT,
        )
        print_colored(
            f"Encrypted Morse Code: {morse_code}", color=Fore.CYAN, style=Style.BRIGHT
        )

    elif args.decrypt:
        morse_code_to_decrypt = args.decrypt
        decrypted_text = morse_to_text(morse_code_to_decrypt)
        print_colored(
            f"Morse Code to Decrypt: {morse_code_to_decrypt}",
            color=Fore.CYAN,
            style=Style.BRIGHT,
        )
        print_colored(
            f"Decrypted Message: {decrypted_text}", color=Fore.GREEN, style=Style.BRIGHT
        )

    if args.play:
        print_colored(
            "Please Wait! Playing Sound...", color=Fore.RED, style=Style.BRIGHT
        )
        if args.encrypt:
            play_morse_code(morse_code)
        elif args.decrypt:
            play_morse_code(morse_code_to_decrypt)


if __name__ == "__main__":
    main()
