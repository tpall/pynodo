import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pynodo",
    version="0.1",
    description="Python wrapper for Zenodo REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tpall/zenapi",
    author="Taavi Päll",
    author_email="tapa741@gmail.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
