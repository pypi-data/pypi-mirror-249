from setuptools import setup, find_packages

with open("README.md") as f:
    description = f.read()

setup(
    name='rawhttpy',
    version='0.1',
    packages=find_packages(),
    entry_points = {'console_scripts': ['rawhttpy = rawhttpy.rawhttpy_cli:main']},
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/0xyy66/RawHTTPy'
)