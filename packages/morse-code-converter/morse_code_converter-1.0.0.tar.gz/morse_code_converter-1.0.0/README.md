# Morse Code Converter
[![Build Status](https://github.com/prashantpandey9/morse-code-converter/workflows/tests_and_coverage/badge.svg)](https://github.com/prashantpandey9/morse-code-converter/actions)
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/your-username/your-repository/actions)


<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/repo-size/prashantpandey9/morse-code-converter)
![GitHub contributors](https://img.shields.io/github/contributors/prashantpandey9/morse-code-converter)
![GitHub stars](https://img.shields.io/github/stars/prashantpandey9/morse-code-converter?style=social)
![GitHub forks](https://img.shields.io/github/forks/prashantpandey9/morse-code-converter?style=social)

A Python package for converting words and sentences to Morse code and playing them in Minion style.

## Features

- Convert text to Morse code.
- Play Morse code in Minion style (requires sound support).
- Reverse translation from Morse code to text.

## Installing Morse Code Converter

To install Morse Code Converter, follow these steps:

Linux, macOS and Windows:
```bash
pip install morse-code-converter
```

## Using Morse Code Converter

To use Morse Code Converter, follow these steps:

```python
from morse_code.converter import text_to_morse, play_morse_code

# Convert text to Morse code
text = "Hello, World!"
morse_code = text_to_morse(text)
print(f"Text: {text}")
print(f"Morse Code: {morse_code}")

# Play Morse code
play_morse_code(morse_code)
```

## Command Line Interface (CLI)
```bash
morse --encrypt "Hello, World!" --play
morse -e "Hello, World!" -p
morse --decrypt ".... . .-.. .-.. ---  .-- --- .-. .-.. -.." --play
morse -d ".... . .-.. .-.. ---  .-- --- .-. .-.. -.." -p
```

## Options
```bash
--encrypt or -e: Encrypt a message to Morse code.
--decrypt or -d: Decrypt Morse code to a message.
--play or -p: Play the Morse code as sound.
```

## Requirements
- Python 3.x
- pygame (for sound playback)
- coverage (for calculating code coverage)

## Contributing to Morse Code Converter
Contributions are welcome! Please open an issue or submit a pull request with improvements.

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin morse-code-converter/<location>`
5. Create the pull request.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
