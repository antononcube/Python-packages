import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RandomSparseMatrix",
    version="0.1.0",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Package for creation of sparse matrices (SSparseMatrix objects.)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/RandomSparseMatrix",
    packages=setuptools.find_packages(),
    install_requires=['SSparseMatrix', 'RandomDataGenerators', 'SparseMatrixRecommender'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["sparse", "matrix", "r", "s", "s-plus", "linear algebra", "linear", "algebra",
              "row names", "column names", "named rows", "named columns"],
    python_requires='>=3.7',
)