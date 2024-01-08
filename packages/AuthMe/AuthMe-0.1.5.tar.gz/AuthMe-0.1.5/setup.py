from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name='AuthMe',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'PyJWT',
        'psycopg2',
    ],
    author='Soumit Das',
    author_email='its.soumit.das@gmail.com',
    description='A python authentication package to work with postgresql, inspired from devise gem for ruby.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
