import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DataTypeSystem",
    version="0.1.1",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Data type system for different data structures (arrays, lists of dictionaries, etc.).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/DataTypeSystem",
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
    keywords=["data structure","type system","types"],
    package_data={},
    python_requires='>=3.7',
)
