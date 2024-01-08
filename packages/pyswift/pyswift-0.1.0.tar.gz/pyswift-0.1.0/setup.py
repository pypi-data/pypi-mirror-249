from setuptools import setup, find_packages

setup(
    name='pyswift',
    version='0.1.0',
    description=open("pyswift/README.md", "r").read(),
    author='TomrisProject',
    requires=["pydantic"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyswift = pyswift.__main__:main',
        ],
    },
    url="https://github.com/TomrisProject/PySwift",
)