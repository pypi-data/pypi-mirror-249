from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="ctype",
    version="7.4.2",
    description="Interact with cython, python, ctypes, and use other c/c++ tools",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/notepads/ctype",
    author="notepads",
    author_email="notepads.py@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Development Status :: 4 - Beta",
        "Development Status :: 3 - Alpha",
        "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Typing :: Typed",
    ],
    keywords="ctype, ctypes, cython, cpython, cpy, python, c, c++",
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    include_package_data=True,
    python_requires=">=3.7"
)