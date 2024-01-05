from setuptools import setup, find_packages

setup(
    name='fastapirichlogger',
    version='0.1.0',
    author='Kevin Saltarelli',
    author_email='kevinqz@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/kevinqz/fastapirichlogger',
    license='LICENSE.md',
    description='An awesome logger for FastAPI.',
    long_description=open('README.md').read(),
    install_requires=[
        "fastapi",
        "rich",
    ],
)