import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LLMPrompts",
    version="0.1.0",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Facilitating the creation, storage, retrieval, and curation of LLM prompts.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/LLMPrompts",
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
    keywords=["prompt", "prompts", "large language model", "large language models", "llm"],
    package_data={'': ['resources/*.json']},
    python_requires='>=3.7',
)
