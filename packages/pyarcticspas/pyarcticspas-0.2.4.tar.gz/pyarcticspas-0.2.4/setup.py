import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pyarcticspas",
    version="0.2.4",
    description="A high-level client library for accessing Arctic Spas API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=["arcticspas >= 2.0"],
    package_data={"pyarcticspas": ["py.typed"]},
)
