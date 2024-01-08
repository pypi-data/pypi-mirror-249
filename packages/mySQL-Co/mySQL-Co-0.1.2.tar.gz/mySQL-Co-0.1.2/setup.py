
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mySQL_Co']

package_data = \
{'': ['*']}


setup_kwargs = {
    'name' :'mySQL-Co',
    'version':'0.1.2',
    'author':'Kasra-Khaksar',
    'author_email':'ksra13khaksar@gmail.com',
    'description':'This is mysql saver , partition , set primary key and update with dataframe',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)