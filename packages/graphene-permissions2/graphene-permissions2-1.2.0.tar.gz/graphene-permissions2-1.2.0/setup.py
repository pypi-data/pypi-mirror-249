from setuptools import setup

from graphene_permissions2 import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements/requirements.txt") as f:
    install_requirements = f.readlines()

setup(
    name="graphene-permissions2",
    packages=("graphene_permissions2",),
    license="MIT",
    version=__version__,
    author="vintersnow",
    description="Simple graphene-django permission system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vintersnow/graphene-permissions",
    install_requires=install_requirements,
    keywords="graphene django permissions permission system",
    python_requires=">=3.10",
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Environment :: Web Environment",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 4.0",
        "Topic :: Internet :: WWW/HTTP",
        "Intended Audience :: Developers",
    ),
)
