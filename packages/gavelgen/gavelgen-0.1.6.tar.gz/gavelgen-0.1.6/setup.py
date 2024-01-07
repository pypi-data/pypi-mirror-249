from setuptools import setup, find_packages

setup(
    name='gavelgen',
    version='0.1.6',
    packages=find_packages(),
    description='GavelGen SDK to log and score interactions',
    author_email='guoyang@gavel.com',
    author="gavelgen",
    install_requires=[
        'requests',
        'pydantic',
    ],
    
)
