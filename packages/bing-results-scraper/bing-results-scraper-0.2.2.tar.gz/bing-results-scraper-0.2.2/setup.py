from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='bing-results-scraper',
    version='0.2.2',
    py_modules=['bing_results_scraper.bing_scraper'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'asyncio',
        'aiohttp',
        'nest-asyncio'
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
