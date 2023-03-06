from setuptools import find_packages, setup

setup(
    name='NotionBot',
    version='0.0.8',
    author='Quan',
    author_email='quan787887@gmail.com',
    packages=find_packages(),
    url='https://github.com/quan0715/PyNotion',
    license='license.txt',
    description='Wrapper around Notion API.',
    # long_description=open('ReadMe.md').read(),
    install_requires=[
        "requests >= 2.18.4"
    ],
)
