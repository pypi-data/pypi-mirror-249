from setuptools import setup, find_packages

setup(
    name="common-library",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dateutil",
        "google-cloud-bigquery"
    ],
)