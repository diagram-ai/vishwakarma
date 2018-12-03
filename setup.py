import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setup(
    name='vishwakarma',
    version='0.0.1',
    description='Python visualization library for Probabilistic Graphical Models, and a lot more!',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/diagram-ai/vishwakarma',
    author='Diagram AI, LLP',
    author_email='notes@diagram.ai',
    maintainer='Diagram AI, LLP',
    maintainer_email='notes@diagram.ai',
    license='MIT',
    keywords=[
        'PGM',
        'pgmpy',
        'visualization',
        'probabilistic-graphical-models',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(
        exclude=(
            "tests",
        )),
    include_package_data=True,
)