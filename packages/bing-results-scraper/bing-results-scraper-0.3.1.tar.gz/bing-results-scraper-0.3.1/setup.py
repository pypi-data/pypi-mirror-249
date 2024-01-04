from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
with open("LICENSE.txt", "r") as fi:
    license_txt = fi.read()

setup(
    name='bing-results-scraper',
    version='0.3.1',
    author='Renukumar R',
    author_email='renu2babu1110@gmail.com',
    license=license_txt,
    py_modules=['bing_results_scraper.bing_scraper'],
    install_requires=[
        'requests==2.31.0',
        'beautifulsoup4==4.12.2',
        'asyncio==3.4.3',
        'aiohttp==3.8.4',
        'nest-asyncio==1.5.6'
    ],
    entry_points={
        'console_scripts': [
            'bing-results-scraper=bing_results_scraper.bing_scraper:main',
        ],
    },
    description='Bing Search Scraper - A Python library for retrieving search results from Bing',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
