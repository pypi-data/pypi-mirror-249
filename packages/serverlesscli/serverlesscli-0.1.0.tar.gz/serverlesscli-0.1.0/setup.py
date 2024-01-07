from setuptools import setup,find_packages

with open('requirement.txt','r') as f:
    requires=f.read().splitlines()

setup(
    name='serverlesscli',
    version='0.1.0',
    author="Raja Ram S",
    author_email="rram91923@gmail.com",
    description="automate db using csv data manipulation",
    packages=find_packages(),
    install_requires=requires,
    entry_points={
        'console_scripts':[
            'serverlesscli=serverlesscli.serverlesscli:main'
        ]
    },
    package_data={
        'serverlesscli': ['*.json', '*.csv'],
    },
)