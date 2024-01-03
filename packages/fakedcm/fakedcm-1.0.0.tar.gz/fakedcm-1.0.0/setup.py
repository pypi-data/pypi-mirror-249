from setuptools import setup

setup(
    name='fakedcm',
    version='1.0.0',
    packages=['fakedcm'],
    install_requires=[
        'fake-useragent',
    ],
    entry_points={
        'console_scripts': [
            'fakedcm = fakedcm.fakedcm:main',
        ],
    },
)
