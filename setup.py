import os

from setuptools import setup

# Using vbox, hard links do not work
if os.environ.get('USER','') == 'vagrant':
    del os.link

with open('README.md', 'r') as fp:
    longdesc = fp.read()

setup(
    name='python-launchpad',
    version='0.1.0',
    description='Control a Novation Launchpad with Python',
    long_description=longdesc,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
    ],
    url='https://github.com/BasementCat/launchpad-python',
    author='Alec Elton',
    author_email='alec.elton@gmail.com',
    license='',
    packages=['launchpad'],
    install_requires=['mido', 'python-rtmidi'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)