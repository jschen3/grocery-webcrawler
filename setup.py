from setuptools import setup

setup(name="grocerywebcrawler", entry_points={
    'console_scripts': [
        'grocerywebcrawler = GroceryWebcrawler:main',
    ],
})
