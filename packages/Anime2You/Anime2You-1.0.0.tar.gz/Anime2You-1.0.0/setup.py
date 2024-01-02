import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = '1.0.0'

setup(
    name='Anime2You',
    long_description=README,
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=[
        "anime2you",
    ],
    url='https://github.com/princessmiku/anime2you',
    license='MIT',
    author='Miku',
    author_email='',
    description='Unofficial RSSClient for Anime2You',
    keywords=['anime2you', 'rss', 'news', 'anime', 'rssclient', 'german'],
    python_requires='>=3.7.0',
    install_requires=[
        'feedparser>=6.0.11',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
