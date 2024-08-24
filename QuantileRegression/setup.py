import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="QuantileRegression",
    version="0.1.4",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="QuantileRegression package based on SciPy optimization routines.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/QuantileRegression",
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
    keywords=["quantile regression", "quantile", "regression", "optimization", "fit", "fitting"],
    python_requires='>=3.7',
)
