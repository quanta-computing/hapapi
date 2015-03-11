"""
Setuptools script for pwatch

"""
from setuptools import setup, find_packages

def readme():
    """
    Extracts readme contents

    """
    with open('README.md') as f:
        return f.read()

def requirements():
    """
    Extacts requirements.txt contents

    """
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='hapapi',
    version='0.1.2',
    description='HAproxy RESTful API',
    long_description=readme(),
    license='MIT',
    url='https://github.com/quanta-computing/hapapi',
    author="Matthieu 'Korrigan' Rosinski",
    author_email='mro@quanta-computing.com',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: System :: Systems Administration',
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hapapi = hapapi.__main__:main',
        ],
    },
    install_requires=requirements(),
)
