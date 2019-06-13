from setuptools import setup, find_packages

setup(
    name="Discord MVC",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "jinja2",
        "click",
        "sqlalchemy",
        "discord"
    ]
)
