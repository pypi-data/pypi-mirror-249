from setuptools import setup


def get_version():
    version = {}
    with open("pecheny_utils/version.py") as f:
        exec(f.read(), version)
    return version["__version__"]


long_description = (
    """Some common utils that I (https://gitlab.com/peczony) use in several projects."""
)


setup(
    name="pecheny_utils",
    version=get_version(),
    author="Alexander Pecheny",
    author_email="ap@pecheny.me",
    description="Utils for my projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/peczony/pecheny_utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pecheny_utils"],
    install_requires=["requests"],
)
