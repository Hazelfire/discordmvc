"""
File: util.py
Author: Sam Nolan
Email: sam.nolan@rmit.edu.au
Github: https://github.com/Hazelfire
Description: Util file for constructing discord.py clients from projects
"""

import asyncio
from importlib import import_module
from collections import namedtuple
import discord
from sqlalchemy import create_engine
from jinja2 import Environment, PackageLoader, select_autoescape
from sqlalchemy.orm import sessionmaker
from .reqs import always
from .routes import group


async def run_routes(routes, message, client, context):
    """Runs the given routes with the message
    :routes: an array of route objects
    :message: Discord.py message

    """

    view = routes(client, message, context)
    if view:
        generator = view(client, message, context)
        action = generator.send(None)
        try:
            while True:
                reply = await action(client, message, context, view.__name__)
                action = generator.send(reply)
        except StopIteration:
            pass


def wrap_bot(on_message):
    """Creates a bot from an async on_message function

    :on_message: async discord.py on_message function
    :returns: Discord.py Client

    """
    client = discord.Client()
    client.event(on_message(client))
    return client


Context = namedtuple("Context", ["templates", "db"])


async def alogin(bots):
    """ Returns a list of logged in bots based off the application settings """
    clients = [create_client(bot) for bot, token in bots]
    
    await asyncio.gather(
        *[client.login(bot[1]) for client, bot in zip(clients, bots)]
    )

    return clients


async def get_bots(module):
    """ Async call that returns all the bots """
    settings = import_module(module)
    applications = settings.APPLICATIONS
    return await alogin(applications)


def create_client(module):
    """Creates a discord client based off project settings
    :returns: Discord.py client

    """
    routes = __import__(module + ".routes").routes.routes
    templates = Environment(
        loader=PackageLoader(module, "templates"), autoescape=select_autoescape([])
    )
    engine = create_engine("sqlite:///db.sqlite3")
    Session = sessionmaker(bind=engine)

    models = __import__(module + ".models").models

    models.Base.metadata.create_all(engine)

    def wrapper(client):
        async def on_message(message):
            """Discord.py on_message function

            :message: Discord.py message

            """
            session = Session()
            templates.globals["message"] = message

            await run_routes(routes, message, client, Context(templates, session))
            session.commit()

        return on_message

    return wrap_bot(wrapper)
