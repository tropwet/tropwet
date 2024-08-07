import glob
import os

import setuptools

import tropwet

setuptools.setup(
    name="tropwet",
    version=tropwet.TROPWET_VERSION,
    description="Tropical Wetland (TropWet) mapping tool.",
    author="Andy Hardy, Greg Oakes and Pete Bunting",
    author_email="ajh13@aber.ac.uk",
    include_package_data=True,
    #scripts=glob.glob("bin/*.py"),
    packages=["tropwet"],
    license="LICENSE.txt",
    install_requires=["earthengine-api"],
    url="https://github.com/tropwet/tropwet",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
