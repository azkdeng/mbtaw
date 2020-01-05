from setuptools import setup
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

__version__ = None
with open(os.path.join(BASE_DIR, 'mbtaw', '__init__.py')) as f:
    exec(f.read())

with open(os.path.join(BASE_DIR, 'README.md')) as f:
    README = f.read()

with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

with open(os.path.join(BASE_DIR, 'test_requirements.txt')) as f:
    TEST_REQUIREMENTS = f.read().splitlines()

setup(
    name='mbtaw',
    version=__version__,
    url='https://github.com/azkdeng/mbtaw',
    description='Python wrapper for MBTA API v3',
    long_description=README,
    author='Alex Deng',
    author_email='azkdeng@gmail.com',
    license='MIT',
    packages=['mbtaw'],
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
)
