"""
File: __init__.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Entry point for discordmvc module
"""
from .util import get_bots

from .cli import cli

def run():
    """ Runs the main management cli """
    cli()
