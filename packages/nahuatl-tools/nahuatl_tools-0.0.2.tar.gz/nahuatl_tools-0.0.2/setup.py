from setuptools import setup

VERSION = '0.0.2'
DESCRIPTION = 'A selection of open source tools for Nahuatl NLP.'

setup(
    name="nahuatl_tools",
    author_email="<nicocloutier1@gmail.com>",
    description=DESCRIPTION,
    version=VERSION,
    long_description_content_type="text/markdown",
    packages=['nahuatl_tools'],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)