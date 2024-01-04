from setuptools import setup, find_packages

VERSION = '0.2.2'
DESCRIPTION = 'Graphite Bridge'
LONG_DESCRIPTION = 'Graphite Bridge'

# Setting up
setup(
    name="graphite-bridge",
    version=VERSION,
    author="Jonathan Wengel",
    author_email="<jonthan.anodaram@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['websocket-client', 'requests'],
    keywords=['python', 'graphite', 'trading', 'cryptocurrency'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
