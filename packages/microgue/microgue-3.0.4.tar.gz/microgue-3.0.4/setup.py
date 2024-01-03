from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="microgue",
    version="3.0.4",
    author="Michael Hudelson",
    author_email="michaelhudelson@gmail.com",
    description="This project contains bootstrap code to speed up the development of AWS based microservices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "flask",
        "flask-classful",
        "redis",
        "requests"
    ],
    python_requires=">=3.6",
)
