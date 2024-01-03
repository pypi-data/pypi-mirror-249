from setuptools import setup, find_packages

setup(
    name='hf_dataset_structurer',
    version='0.0.1',
    description='',
    install_requires=[
        'datasets',
        'Jinja2',
        'huggingface-hub'
    ],
    packages=find_packages(),
    author='Rúben Almeida'
)
