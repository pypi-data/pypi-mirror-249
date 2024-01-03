import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "idev-pytermcolor",
    version = "1.0.0",
    author = "IrtsaDevelopment",
    author_email = "irtsa.development@gmail.com",
    description = "A python collection of functions to print of colored text to console / terminal.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/IrtsaDevelopment/PyTermColor",
    project_urls = {
        "Bug Tracker": "https://github.com/IrtsaDevelopment/PyTermColor/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "idev-pytermcolor"},
    packages=["PyTermColor"],
    python_requires = ">=3.6"
)