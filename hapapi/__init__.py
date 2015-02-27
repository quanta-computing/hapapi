"""
Main entry points and resources for hapapi

"""
from flask import Flask

VERSION = '0.1'

app = Flask('hapapi')
config = {
    'token': 'suce',
}
