from setuptools import setup, find_packages

setup(
    name='skymap_job_processing',
    version='0.4.0',
    packages=find_packages(),
    install_requires=[
        "requests",
        "websockets"
    ],
)