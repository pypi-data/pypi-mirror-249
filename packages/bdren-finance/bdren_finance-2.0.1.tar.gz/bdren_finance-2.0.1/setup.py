from pathlib import Path

from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='bdren_finance',
    version='2.0.1',
    author='Shuvo',
    author_email='shuvo.punam@gmail.com',
    description='BdREN Finance',
    packages=find_packages(
        include=[
            'bdren_finance',
            'bdren_finance.*',
        ]
    ),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
        'Django',
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
