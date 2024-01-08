import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "i2clcdcon",
    version = "0.0.1",
    author = "Evan",
    author_email = "ecarns31@gmail.com",
    description = "Controlling an i2c lcd1602 device",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Evanc09/LCDCON",
    project_urls = {
        "Bug Tracker": "https://github.com/Evanc09/LCDCON/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.9"
)