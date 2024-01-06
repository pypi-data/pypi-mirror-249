from setuptools import setup, find_packages
from package.version import version


# Function to read the list of dependencies from requirements.txt
def read_requirements():
    with open('./requirements.txt') as req:
        return req.read().splitlines()


setup(
    name="codara",
    version=version,
    packages=find_packages(),
    description="AI Code Review Automation Tool",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "codara=package.app:main"
        ]
    }
)
