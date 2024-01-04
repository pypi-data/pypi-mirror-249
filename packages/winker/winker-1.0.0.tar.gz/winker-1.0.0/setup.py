from setuptools import setup, find_packages

setup(
    name='winker',
    version='1.0.0',
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
)
