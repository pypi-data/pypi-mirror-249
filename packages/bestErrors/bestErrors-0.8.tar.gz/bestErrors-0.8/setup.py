from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    desc = f.read()

setup(
    name='bestErrors',
    version='0.8',
    packages=find_packages(),
    long_description=desc,
    long_description_content_type='text/markdown',
    requires=[
        'erodecor'
    ]
)