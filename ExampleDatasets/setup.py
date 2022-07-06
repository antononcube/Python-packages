import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ExampleDatasets",
    version="0.1.1",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Example datasets from statistics packages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/ExampleDatasets",
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'xdg'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["data frame", "dataset", "example", "example dataset", "Rdatasets"],
    package_data={'': ['resources/*.csv.gz']},
    python_requires='>=3.7',
)
