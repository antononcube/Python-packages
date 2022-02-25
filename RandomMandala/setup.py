import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RandomMandala",
    version="0.6.0",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Generator of random mandalas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/RandomMandala",
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'matplotlib', 'bezier', 'pillow'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Artistic License",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
    ],
    keywords=["random", "mandala", "random mandala", "mandala diagram", "image generation", "generative art"],
    python_requires='>=3.7',
)
