from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
readme = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="ctype",
    version="0.0.0",
    description="ctype.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ctype/ctype",
    author="ctype",
    #author_email="oqibz@example.com",
    license="MIT",
    classifiers=[

    ],
    packages=find_packages(exclude=["ctype.tests", "ctype.tests.*", "tests"]),
    include_package_data=True,
    install_requires=["typing"],
    python_requires=">=3.7",
)