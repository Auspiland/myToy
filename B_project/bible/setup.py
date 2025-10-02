# -*- coding: utf-8 -*-
"""
Setup script for BOJ Bible
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="boj-bible",
    version="1.0.0",
    author="BOJ Bible Contributors",
    author_email="",
    description="Competitive Programming Library for Python - Data Structures and Algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/boj-bible",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="competitive programming, algorithms, data structures, boj, online judge",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/boj-bible/issues",
        "Source": "https://github.com/yourusername/boj-bible",
        "Documentation": "https://github.com/yourusername/boj-bible/wiki",
    },
    install_requires=[
        # No external dependencies - pure Python library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.900",
        ],
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)