import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zenapi",
    version="0.2",
    description="Python wrapper for Zenodo REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tpall/zenapi",
    author="Taavi Päll",
    author_email="tapa741@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    zip_safe=False,
)
