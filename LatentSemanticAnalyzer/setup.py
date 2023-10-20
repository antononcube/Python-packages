import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LatentSemanticAnalyzer",
    version="0.1.2",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Latent Semantic Analysis package based on \"the standard\" Latent Semantic Indexing theory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/LatentSemanticAnalyzer",
    install_requires=['numpy', 'scipy', 'pandas', 'stop-words', 'snowballstemmer', 'nimfa',
                      'SSparseMatrix', 'SparseMatrixRecommender'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords=["sparse", "matrix", "sparse matrix",
              "linear algebra", "linear", "algebra",
              "lsi", "latent semantic indexing",
              "dimension", "reduction", "dimension reduction",
              "svd", "singular value decomposition",
              "nnmf", "nmf", "non-negative matrix factorization"],
    package_data={'': ['resources/*.csv', 'resources/*.csv.gz']},
    python_requires='>=3.7',
)
