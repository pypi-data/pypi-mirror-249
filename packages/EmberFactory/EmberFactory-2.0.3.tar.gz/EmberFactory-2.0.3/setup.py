from setuptools import setup

def getversion():
    with open('emberfactory/__init__.py') as fp:
        for line in fp:
            if line.startswith('__version__'):
                return line.split("'")[1]
    return None

setup(version=getversion())
