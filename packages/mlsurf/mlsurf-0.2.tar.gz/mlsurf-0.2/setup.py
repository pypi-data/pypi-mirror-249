from setuptools import setup, find_packages

setup(
    name='mlsurf',
    author='freebiesoft',
    version='0.2',
    packages=find_packages(exclude=('tests', 'tests.*', '00', '00.*')),
    # Add more information here as needed
)
