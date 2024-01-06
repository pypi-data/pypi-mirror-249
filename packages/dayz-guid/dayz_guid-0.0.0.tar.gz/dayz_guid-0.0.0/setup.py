from setuptools import setup

"""
:authors: CRX
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2024 CRX
"""

version = ''
'''
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()
'''

long_description = '''Python module for dayz-guid 
                    steam64id converter to game GUID from Dayz or BE'''

setup(
    name='dayz_guid',
    version=version,

    author='CRX',
    autjor_email='cherniq66@gmail.com',

    description=(
        u'Python module to convert steam id to dayz guid or battleeye guid '
        u'dayz-guid (Converter)'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",

    license='Apache License, Version 2.0, see LICENSE file',

    packages=['dayz-guid'],

    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers'
    ]
)
