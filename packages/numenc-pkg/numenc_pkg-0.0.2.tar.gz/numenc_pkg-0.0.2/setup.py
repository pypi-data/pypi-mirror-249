from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'Number Encryptor that encrypts and decrypts your pin'
# LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="numenc_pkg",
    version=VERSION,
    author="Chirag Shah",
    author_email="chirag.h.shahh@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['enc', 'encryptor', 'pin', 'code', 'decryptor', 'password'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)