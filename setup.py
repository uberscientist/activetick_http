from activetick_http import __version__
from os import path

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(path.join(path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

setup(
    name='activetick_http',
    version=__version__,
    description='Pandas wrapper for ActiveTick HTTP Proxy',
    long_description=long_description,
    url='https://github.com/uberscientist/activetick_http',
    author='Christopher Toledo',
    author_email='chris@mindsforge.com',
    keywords=['activetick', 'finance', 'quant', 'pandas'],
    license='MIT',
    packages=['activetick_http'],
    tests_require=['pytest',
                   'tabulate',
                   'redis'
    ],
    package_dir={'activetick_http': 'activetick_http'},
    install_requires=[
        'pandas',
        'requests',
        'numpy',
        'redis'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ]
)
