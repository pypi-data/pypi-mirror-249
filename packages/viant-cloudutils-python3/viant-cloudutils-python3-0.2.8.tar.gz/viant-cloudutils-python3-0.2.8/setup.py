import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setuptools.setup(
    name="viant-cloudutils-python3",
    version="0.2.8",
    author="Lee Sautia",
    author_email="lsautia@viantinc.com",
    description="Cloud utilities for automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.vianttech.com/techops/cloudutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS
)
