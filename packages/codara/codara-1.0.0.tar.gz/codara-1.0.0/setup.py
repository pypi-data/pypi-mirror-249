from setuptools import setup, find_packages


# Function to read the list of dependencies from requirements.txt
def read_requirements():
    with open('./requirements.txt') as req:
        return req.read().splitlines()


setup(
    name="codara",
    version="1.0.0",
    packages=find_packages(),
    description="AI Code Review Automation Tool",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "codara=package.app:main"
        ]
    }
)
