from setuptools import setup
import setuptools


setup(
    name='os-notify',  # Name of your package
    author='Aly Mohamed',
    author_email='alyhassan10@hotmail.com',
    version='0.2.0',  # Package version
    entry_points={
        'console_scripts': [
            'notify=notify:main',  # Create the console script entry point
        ],
    },
    url="https://github.com/alymohamedhassan/databaser",
    project_urls={
        "Bug Tracker": "https://github.com/alymohamedhassan/databaser/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
