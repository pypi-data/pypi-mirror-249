from setuptools import setup, find_packages

setup(
    name='ptrack',
    version="2.0.3",
    description='A simple CLI utility for asthetically tracking progress when copying, moving or downloading files.',
    author='Connor Etherington',
    author_email='connor@concise.cc',
    packages=find_packages(),
    install_requires=[
        "ascii_magic",
        "beautifulsoup4",
        "Pillow",
        "Requests",
        "rich",
        "yt_dlp",
        "humanize",
        "validators",
    ],
    entry_points={
        'console_scripts': [
            'ptc=ptrack.main:copy',
            'ptm=ptrack.main:move',
            'ptd=ptrack.main:download',
            'ptrack=ptrack.main:main',
        ]
    }
)
