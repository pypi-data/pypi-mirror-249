from setuptools import setup, find_packages

long_description = "Tool for reducing pdf file size"

setup(
    name='reduce_pdf',
    version='0.0.1',
    description='Tool for reducing pdf file size',
    author='Mochan Shrestha',
    packages=['reduce_pdf'],
    install_requires=[
        'pillow',
        'PyMuPDF',
    ],
    long_description=long_description,
    scripts=['bin/reduce-pdf'],
)
