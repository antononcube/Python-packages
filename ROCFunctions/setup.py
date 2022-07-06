import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ROCFunctions",
    version="0.1.2",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Receiver Operating Characteristic (ROC) functions package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/ROCFunctions",
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
    keywords=["roc", "receiver operating characteristic", "classifier", "classification",
              "ml", "machine learning"],
    python_requires='>=3.7',
)
