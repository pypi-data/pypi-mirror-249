from setuptools import setup, find_packages

setup(
    name='hf_dataset_structurer',
    version='0.0.6',
    description='A package to structure datasets in the Hugging Face Hub',
    url='https://github.com/arubenruben/hf_dataset_structurer',
    author_email="ruben.f.almeida@inesctec.pt",
    license='MIT',
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
