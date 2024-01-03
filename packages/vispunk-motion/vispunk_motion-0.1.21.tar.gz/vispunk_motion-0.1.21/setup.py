import vispunk_motion
from setuptools import setup, find_packages

version = vispunk_motion.__version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="vispunk_motion",
    packages=find_packages(exclude=[]),
    package_data={'': ['**/*.json', '**/*.txt']},
    version=version,
    description=(
        "Vispunk. "
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="The Vispunk Authors",
    author_email="limsweekiat@gmail.com",
    url="https://github.com/greentfrapp/lucent",
    license="Apache License 2.0",
    keywords=[
        "pytorch",
        "tensor",
        "machine learning",
        "neural networks",
        "convolutional neural networks",
        "feature visualization",
        "optimization",
    ],
    install_requires=[
        "torch>=1.13.0",
        "diffusers",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)