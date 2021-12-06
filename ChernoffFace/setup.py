import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ChernoffFace",
    version="0.1.0",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Makes of Chernoff face diagrams.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/ChernoffFace",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib', 'pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Artistic License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
