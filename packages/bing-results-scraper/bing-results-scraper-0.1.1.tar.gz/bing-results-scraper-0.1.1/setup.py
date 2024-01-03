from setuptools import setup

setup(
    name='bing-results-scraper',
    version='0.1.1',
    packages=['bing_results_scraper'],
    install_requires=[
        'requests',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'bing-results-scraper=bing_results_scraper.bing_results_scraper:main',
        ],
    },
    description='A Python library for scraping Bing search results',
    long_description='A simple and easy-to-use Python library for scraping Bing search results.',
    long_description_content_type='text/markdown',  # Use 'text/plain' if not using Markdown
)
