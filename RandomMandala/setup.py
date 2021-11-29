import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RandomMandala",
    version="0.5.1",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Generator of random mandalas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/RandomMandala",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib', 'bezier', 'pillow'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Artistic License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
