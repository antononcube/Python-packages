import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SparseMatrixRecommender",
    version="0.1.8",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Sparse Matrix Recommender package based on SSparseMatrix objects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/SparseMatrixRecommender",
    install_requires=['numpy', 'scipy', 'SSparseMatrix', 'pandas'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords=["sparse", "matrix", "recommender", "sparse matrix recommender",
              "linear algebra", "linear", "algebra",
              "recommendations"],
    package_data={'': ['resources/*.csv', 'resources/*.csv.gz']},
    python_requires='>=3.7',
)