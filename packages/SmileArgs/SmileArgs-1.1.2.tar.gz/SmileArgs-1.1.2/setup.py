#import setuptools
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="SmileArgs",
    version="1.1.2",
    author="Sitthykun LY",
    author_email="ly.sitthykun@gmail.com",
    description="It is a modern args catching with python3 and OOP structure and implementation.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/sitthykun/smileargs",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
        	"Programming Language :: Python :: 3.11",
		"Programming Language :: Python :: 3.12",
		"License :: OSI Approved :: MIT License",
        	"Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
    ],
)
