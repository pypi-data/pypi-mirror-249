from setuptools import setup

setup(
    name="convertnotes",
    version="0.1",
    scripts=["main.py"],
    description="Converts notes from one application to another",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Daniel Posthuma",
    author_email="dnjp@posteo.org",
    url="https://github.com/dnjp/convertnotes",
    install_requires=["nanoid"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
    ],
    python_requires=">=3.11",
)
