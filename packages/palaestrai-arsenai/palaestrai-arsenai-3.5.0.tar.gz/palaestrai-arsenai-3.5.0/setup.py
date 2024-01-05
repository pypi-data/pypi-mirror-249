#!/usr/bin/env python3
"""Setup file for the ARL package."""
import setuptools

with open("VERSION") as freader:
    VERSION = freader.readline().strip()


with open("README.md") as freader:
    README = freader.read()

install_requirements = [
    "click",
    "numpy",
    "pandas",
    "doepy",
    "ruamel.yaml",
    "palaestrai~=3.5.0",
]

setuptools.setup(
    name="palaestrai-arsenai",
    version=VERSION,
    author="The ARL Developers",
    author_email="stephan.balduin@offis.de",
    description="Adversarial Resilience Learning Design of Experiments.",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requirements,
    license="LGPL",
    entry_points="""
        [console_scripts]
        arsenai=arsenai.cli.arsenai:main
    """,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.10.0",
)
