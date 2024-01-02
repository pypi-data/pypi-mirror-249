"""
Defines the entry point of the extension
"""

import setuptools
import os
import codecs
import io

with io.open("README.md") as readme_file:
    long_description = readme_file.read()

# Register plugin with pytest
setuptools.setup(
    name ='pyunit-spiratest',
    version = '6.0.0',
    author = 'Inflectra Corporation',
    author_email ='support@inflectra.com',
    url = 'http://www.inflectra.com/SpiraTest/Integrations/Unit-Test-Frameworks.aspx',
    description = 'Exports Python unit tests as test runs in Spira (SpiraTest/Team/Plan)',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    py_modules = ['spiratestextension', 'spiratestexecute'],
    classifiers = [
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points = {
        'pytest11': [
            'pyunit-spiratest = spiratestextension',
        ],
    },
    include_package_data=True,
    package_data={'': ['testsequencefunctions.py', 'seleniumtest.py']},
)
