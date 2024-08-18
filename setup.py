from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="galactic_dynamics",
    version="0.1.0",
    author="TUstudents",
    author_email="your.email@example.com",
    description="A package for modeling galactic dynamics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tustudents/galactic_dynamics",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10"
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.18.0",
        "scipy>=1.4.0",
        "matplotlib>=3.1.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "sphinx>=3.0"],
    },
    license="CC BY-NC-SA 4.0",
    license_files=("LICENSE",),
)