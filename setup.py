from setuptools import setup

setup(
    name="zenapi",
    version="0.1",
    description="Python wrapper for Zenodo API.",
    url="http://github.com/tpall/zenapi",
    author="Taavi Päll",
    author_email="tapa741@gmail.com",
    license="MIT",
    packages=["zenapi"],
    install_requires=["requests"],
    zip_safe=False,
)
