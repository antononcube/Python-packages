import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DSLTranslation",
    version="0.1.1",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Translation of natural Domain Specific Language (DSL) commands into code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/DSLTranslation",
    packages=setuptools.find_packages(),
    install_requires=["pyperclip"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["dsl", "parser", "interpreter", "code generation", "multi-language", "nlp"],
    python_requires='>=3.7',
)
