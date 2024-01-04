from setuptools import setup, find_packages

setup(
    name='hf_dataset_structurer',
    version='0.0.4',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    install_requires=[
        'datasets',
        'Jinja2',
        'huggingface-hub'
    ],
    packages=find_packages(),
    author='Rúben Almeida'
)
