from setuptools import find_packages
from setuptools import setup

setup(
    name='itde',
    version='1.0.2',
    description='InnerTube Data Extractor',
    author='Simone Gentili',
    author_email='gentilismn@gmail.com',
    python_requires='>=3.6.0',
    url='https://github.com/steghy/itde',
    packages=find_packages(
        exclude=[
            "tests",
            "*.tests",
            "*.tests.*",
            "tests.*"
        ]
    ),
    install_requires=[],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
