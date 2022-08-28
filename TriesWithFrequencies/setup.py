import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TriesWithFrequencies",
    version="0.0.1",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="This package provides tries (prefix trees) with frequencies implementation based on dictionaries.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/TriesWithFrequencies",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["trie", "prefix tree", "frequency", "frequencies"],
    python_requires='>=3.7',
)
