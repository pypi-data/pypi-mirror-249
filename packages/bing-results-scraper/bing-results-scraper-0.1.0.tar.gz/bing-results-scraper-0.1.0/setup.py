from setuptools import setup

setup(
    name='bing-results-scraper',
    version='0.1.0',
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
)