from setuptools import setup, find_packages

setup(
    name='mySQL-Co',
    version='0.0.1',
    author='Kasra-Khaksar',
    author_email='ksra13khaksar@gmail.com',
    description='This is mysql saver , partition , set primary key and update with dataframe',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)