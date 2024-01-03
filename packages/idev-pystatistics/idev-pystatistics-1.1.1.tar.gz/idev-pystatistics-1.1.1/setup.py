import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "idev-pystatistics",
    version = "1.1.1",
    author = "IrtsaDevelopment",
    author_email = "irtsa.development@gmail.com",
    description = "A python collection of classes and functions to help with numbers along with collections of numbers i.e., statistics.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/IrtsaDevelopment/PyStatistics",
    project_urls = {
        "Bug Tracker": "https://github.com/IrtsaDevelopment/PyStatistics/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "idev-pystatistics"},
    packages=["PyStatistics"],
    python_requires = ">=3.6"
)