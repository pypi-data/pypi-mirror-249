from __future__ import absolute_import, division, print_function
from setuptools import setup
from pyco_sqlalchemy import __version__

description = "Simple ORM BaseModel for Flask depends on SqlAlchemy"

try:
    with open("readme.md", "r") as fh:
        readme = fh.read()
except Exception as e:
    readme = description

setup(
    name="pyco_orm",
    url="https://github.com/dodoru/pyco-sqlalchemy",
    license="MIT",
    version=__version__,
    author="Nico Ning",
    author_email="dodoru@foxmail.com",
    description=(description),
    long_description=readme,
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    packages=["pyco_sqlalchemy"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "SQLAlchemy <=1.3.4",
        "Flask-SQLAlchemy <=2.4.0",
        "python-dateutil >=2.8.0",
    ],
    platforms='any',
)
