from setuptools import setup, find_packages

setup(
    name='pythonray',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    # other metadata
    author='Harry Lipnick',
    author_email='harry.lipnick@gmail.com',
    description='A package to send messages to Spatie\'s Ray from Python',
    license='MIT',
    keywords='python ray spatie',
    url='https://github.com/hlipnick/python-ray'
)