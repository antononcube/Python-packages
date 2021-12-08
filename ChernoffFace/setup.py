import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ChernoffFace",
    version="0.1.4",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Makes of Chernoff face diagrams.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/ChernoffFace",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib', 'pillow'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Artistic License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
    ],
    keywords=["chernoff", "face", "chernoff face", "chernoff face diagram", "multi-dimensional", "visualization"],
    package_data={'': ['resources/*.csv']},
    python_requires='>=3.7',
)
