from setuptools import setup, find_packages

# Read the contents of the README file
with open('./fastapirichlogger/README.md', encoding='utf-8') as f:
    long_description = f.read()
  
setup(
    name='fastapirichlogger',
    version='0.1.3',
    author='Kevin Saltarelli',
    author_email='kevinqz@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/kevinqz/fastapirichlogger',
    license='LICENSE.md',
    description='An awesome logger for FastAPI.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        "fastapi",
        "rich",
    ],
)