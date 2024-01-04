import setuptools

VERSION = "0.0.3"
DESCRIPTION = "A user friendly version of the Metatrader5 python library."



with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="BetterMt5",
    version=VERSION,
    author="Mathijs Follon",
    author_email="contact@mfollon.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mathlon26/BetterMt5",
    packages=[
        "BetterMt5",
    ],
    install_requires=[
        "MetaTrader5>=5.0.45"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    keywords=['python', 'trading', 'trader', 'metatrader', 'MetaTrader5', 'daytrading', 'bot', 'expert advisor', 'EA', 'automated'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License"
    ]
)
