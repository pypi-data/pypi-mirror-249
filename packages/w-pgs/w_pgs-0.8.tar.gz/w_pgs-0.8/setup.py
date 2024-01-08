from setuptools import setup, find_packages

setup(
    name="w_pgs",
    version="0.8",
    packages=find_packages(),
    install_requires=[
        "psycopg2",
    ],
    author="woi",
    author_email="willooi@qq.com",
    description="A useless database connection tool based on psycopg2",
    license="MIT",
    keywords="wpgs",
    url="https://github.com/mkitpro/wpgs.git"
)
