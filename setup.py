import sys
from setuptools import setup, find_packages

py26_dependency = []
if sys.version_info <= (2, 6):
    py26_dependency = [
        "argparse >= 1.2.1"
    ]

setup(
    name="astronomer",
    version="0.0.0",
    description="Fetch information about the users who've starred a given GitHub repository.",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3"
    ],
    keywords="github stars starred stargazers",
    author="Jeremy Singer-Vine",
    author_email="jsvine@gmail.com",
    url="http://github.com/jsvine/astronomer/",
    license="MIT",
    packages=find_packages(exclude=["test",]),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        "requests"
    ] + py26_dependency,
    tests_require=[],
    test_suite="test",
    entry_points={
        "console_scripts": [
            "astronomer = astronomer.cli:main",
        ]
    }
)
