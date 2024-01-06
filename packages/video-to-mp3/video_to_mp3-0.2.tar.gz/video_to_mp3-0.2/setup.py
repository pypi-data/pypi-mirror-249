from setuptools import setup, find_packages

setup(
    name='video_to_mp3',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'click==8.1.7',
        'moviepy==1.0.3'
    ],
    entry_points={
        'console_scripts': [
            'video_to_mp3=video_to_mp3.cli:main',
        ],
    },
    long_description_content_type='text/markdown',
    long_description=open('README.rst').read()
)