from setuptools import setup, find_packages

setup(
    name="convertnotes",
    version="0.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "convertnotes = convertnotes.main:main",
        ],
    },
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
