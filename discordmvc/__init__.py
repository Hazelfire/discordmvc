"""
File: __init__.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Entry point for discordmvc module
"""
from .cli import cli
from .util import get_bots


def run(_):
    """ Runs the cli """
    cli()
