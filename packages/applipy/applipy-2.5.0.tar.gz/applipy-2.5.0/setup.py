from os import path

from distutils.util import convert_path
from setuptools import setup, find_packages


ns = {}
ver_path = convert_path("applipy/version.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), ns)
version = ns["__version__"]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="applipy",
    url="https://gitlab.com/applipy/applipy",
    project_urls={
        "Source": "https://gitlab.com/applipy/applipy",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
    ],
    description="Library for building modular applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    author="Alessio Linares",
    author_email="mail@alessio.cc",
    version=version,
    entry_points={
        "console_scripts": [
            "applipy = applipy.__main__:entrypoint",
        ],
    },
    packages=find_packages(exclude=["docs", "tests"]),
    data_files=[],
    python_requires=">=3.9",
    install_requires=["applipy_inject>=1.3.1,<2.0.0"],
    scripts=[],
    package_data={"applipy": ["py.typed"]},
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "mypy==1.8.0",
            "flake8==6.1.0",
            "types-PyYAML",
        ],
    },
)
