import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SSparseMatrix",
    version="0.3.3",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="SSparseMatrix package based on SciPy sparse matrices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/SSparseMatrix",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'scipy'],
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
