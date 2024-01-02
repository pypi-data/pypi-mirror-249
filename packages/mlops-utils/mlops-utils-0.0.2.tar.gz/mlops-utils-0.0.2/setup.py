import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mlops-utils",
    version="0.0.2",
    author="robert-min",
    author_email="robertmin522@gmail.com",
    description="mlops utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FLYAI4/mlops-utils",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "mlflow",
        "scipy",
        ],
    classifiers=[
        "Programming Language :: Python :: 3.10"
    ],
    python_requires='>=3.10',
)