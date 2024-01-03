from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="roadrage",
    version="0.1.1",
    author="Arpit Sengar (arpy8)",
    author_email="arpitsengar99@gmail.com",
    description="A python package developed to play `Road Rage` game from hand gestures.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpy8/roadrage",
    packages=find_packages(),
    install_requires=["mediapipe", "opencv-python", "pyautogui"],
    entry_points={
        "console_scripts": [
            "roadrage=roadrage.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT"
)