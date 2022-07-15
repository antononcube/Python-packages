import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RandomDataGenerators",
    version="0.3.0",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Generator of random data frames.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/RandomDataGenerators",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'pandas', 'StringGenerator'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["random", "random data frame", "random dataset", "dataset", "data", "frame",
              "random pet name", "pet name", "random word", "word",
              "random data generator", "data generators", "random job title", "job title"],
    include_package_data=True,
    package_data={'': ['resources/*.csv']},
    python_requires='>=3.7',
)
