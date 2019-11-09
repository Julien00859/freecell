import setuptools

with open("README.md", "r") as fd:
    long_description = fd.read()

with open("VERSION", "r") as fd:
    version = fd.read().strip()

setuptools.setup(
    name="freecell",
    version=version,
    author="Julien Castiaux",
    author_email="julien.castiaux@gmail.com",
    description="Freecell solitaire game with solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),

    # https://pypi.org/classifiers/
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Games/Entertainment",
    ],
)
