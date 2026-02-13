import setuptools

setuptools.setup(
    name="LLMPrompts",
    version="0.2.0",
    author="Anton Antonov",
    author_email="antononcube@posteo.net",
    description="Facilitating the creation, storage, retrieval, and curation of LLM prompts.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/antononcube/Python-packages/tree/main/LLMPrompts",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    keywords=["openai", "chatgpt", "palm", "prompt", "prompts",
              "large language model", "large language models",
              "llm", "llm prompt", "llm prompts"],
    package_data={'LLMPrompts': ['resources/*.json']},
    python_requires='>=3.7',
    license="BSD-3-Clause"
)