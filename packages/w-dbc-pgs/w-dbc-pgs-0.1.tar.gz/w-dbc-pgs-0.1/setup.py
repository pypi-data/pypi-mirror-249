from setuptools import setup, find_packages

setup(
    name="w-dbc-pgs",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
    ],
    author="Will Ooi",
    author_email="willooi@qq.com",
    description="A useless db connection tool based on psycopg2",
    license="MIT",
    keywords="wpgs",
    url="https://github.com/mkitpro/wpgs.git"
)
