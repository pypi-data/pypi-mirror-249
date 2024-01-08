from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

LONG_DESCRIPTION = 'A package that allows to create payment link, cancel order, confirm webhook and get payment link information'

setup(
    name='payos',
    version='0.1.4',
    author='Casso',
    author_email='hieunt@casso.vn, khanhnm@casso.vn',
    description='A library for create Payment Link of payOS and more',
    long_description_content_type="text/markdown",

    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
        keywords=['payos', 'vietqrpro', 'payos-python', 'vietqr', 'payos', 'qr-pay', 'vietnam-banks'],

)