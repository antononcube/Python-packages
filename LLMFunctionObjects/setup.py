import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LLMFunctionObjects",
    version="0.1.7",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Large Language Models (LLMs) functions package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/LLMFunctionObjects",
    packages=setuptools.find_packages(),
    install_requires=["google-generativeai>=0.3.2", "openai>=1.3.0"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["llm", "llm functions", "llm functors", "large language models", "openai", "chatgpt", 'palm',
              "ml", "machine learning"],
    python_requires='>=3.7',
)
