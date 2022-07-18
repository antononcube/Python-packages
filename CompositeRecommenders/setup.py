import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CompositeRecommenders",
    version="0.0.1",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Composite recommenders based on SparseMatrixRecommender and LatentSemanticAnalyzer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/CompositeRecommenders",
    install_requires=['numpy', 'scipy', 'SSparseMatrix', 'pandas', 'SparseMatrixRecommender', 'LatentSemanticAnalyzer'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords=["sparse", "matrix", "recommender", "sparse matrix recommender",
              "linear algebra", "linear", "algebra",
              "recommendations",  "SMR", "LSA", "composite", "composite design pattern"],
    package_data={},
    python_requires='>=3.7',
)