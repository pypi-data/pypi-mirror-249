from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

VERSION="0.0.1"

setup(
    name='pythonray',
    version=VERSION,
    author='Harry Lipnick',
    author_email='harry.lipnick@gmail.com',
    description='A package to send messages to Spatie\'s Ray from Python',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python','ray','spatie'],
)