from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='winker',
    version='1.0.4',
    packages=find_packages(),
    package_data={'': ['*.html']},
    include_package_data=True,
    author='KVI Kontent',
    author_email='kviappsgames@gmail.com',
    description='A library for creating web apps in Python with futuristic minimalistic design',
    url='https://kvi-kontent.gitbook.io/winker/',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'winker = winker.winker:main'
        ]
    }
)
