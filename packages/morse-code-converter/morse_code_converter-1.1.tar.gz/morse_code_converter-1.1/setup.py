from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="morse_code_converter",
    version="1.1",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "morse=morse_code.minion_mode:main",
        ],
    },
)
