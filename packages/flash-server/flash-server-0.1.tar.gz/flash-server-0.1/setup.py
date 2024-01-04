from setuptools import setup, find_packages

setup(
    name='flash-server',
    version='0.1',
    packages=find_packages(),
    description='A simple http-server written in python that supports file uploads.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='fxfy',
    url='https://github.com/fxfyio/py-http-server',
    install_requires=[
    ],
)
