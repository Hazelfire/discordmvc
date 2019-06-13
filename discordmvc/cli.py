"""
File: cli.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Main cli for discordmvc
"""

from importlib import import_module
import os
import asyncio
import click
from discordmvc.projects import create_project
from .util import create_client


@click.group()
def cli():
    """Main cli group"""


@cli.command()
@click.argument("name")
@click.option("-d", "--directory")
def create(name, directory):
    """Creates a discordmvc project

    :name: the name of the project
    :directory: Optional directory for the project

    """
    create_project(name, directory)


async def arun(bots):
    """ Runs all bots asyncronously """
    await asyncio.gather(*[create_client(bot).start(token) for bot, token in bots])


@cli.command()
def run():
    """ Runs the discord bots """
    settings = import_module(os.environ["DMVC_SETTINGS_MODULE"])
    applications = settings.APPLICATIONS
    print("Running bots")
    asyncio.get_event_loop().run_until_complete(arun(applications))
