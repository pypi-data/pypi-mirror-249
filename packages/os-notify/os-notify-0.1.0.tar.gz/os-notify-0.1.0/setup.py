from setuptools import setup

setup(
    name='os-notify',  # Name of your package
    author='Aly Mohamed',
    author_email='alyhassan10@hotmail.com',
    version='0.1.0',  # Package version
    packages=['src'],  # Include the src directory as a package
    entry_points={
        'console_scripts': [
            'notify=src.notify:main',  # Create the console script entry point
        ],
    },
)
