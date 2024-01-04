from setuptools import setup, find_packages

setup(
    name='hikari-ongaku',
    version='0.1.0',
    author='MPlaty',
    author_email='mplatypus54@gmail.com',
    description='A Music handler, for hikari.',
    packages=find_packages(),
    python_requires='>=3.11',
    requires=["hikari", "aiohttp"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
    ]
)
