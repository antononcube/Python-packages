import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SparseMatrixRecommender-antononcube",
    version="0.1.0",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Sparse Matrix Recommender package based on SSparseMatrix objects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)