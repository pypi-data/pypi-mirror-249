from setuptools import setup, find_packages
import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().split("\n")

setup(
    name="bodosdk",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Bodo, Inc.",
    author_email="noreply@bodo.ai",
    packages=find_packages(include=["bodosdk", "bodosdk.*"]),
    scripts=[],
    url="https://github.com/Bodo-inc/bodo-sdk",
    description="Bodo Platform SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
