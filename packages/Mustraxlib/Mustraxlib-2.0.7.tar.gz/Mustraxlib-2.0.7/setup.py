from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: Other/Proprietary License',
    'Programming Language :: Python :: 3.12',
]

setup(
    name='Mustraxlib',
    version='2.0.7',
    description='Simple tools for convenient programming',
    long_description=open('README.txt', 'r', encoding='utf-8').read() + '\n\n' + open('CHANGELOG.txt', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Programmer101',
    author_email='wsl.com.uk@gmail.com',
    license='Copyright 2023 Programmer101. All rights reserved. See LICENCE.txt for details',
    classifiers=classifiers,
    keywords='Efficiency, User Input, Hashing, Encryption, Matrix, 2D Lists, List Manipulation',
    packages=find_packages(),
    install_requires=['bs4', 'requests', 'argon2-cffi', 'colorama']
)
