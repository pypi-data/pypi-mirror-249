
import setuptools
from pystime.version import __version__

# with open("README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="pystime",
    version=__version__,
    author="Lingxi Chen",
    author_email="chanlingxi@gmail.com",
    description="Tool for spatial tumor immune micro-environment",
    include_package_data=True,
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/compbiocclab/stime",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ]
)
