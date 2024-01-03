from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name='datepy',
    version='0.1.5',
    description='A robust utility for parsing dates in various formats.',
    author='msj121',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "dateparser"
    ],
)

# python setup.py sdist bdist_wheel
# twine upload dist/*      