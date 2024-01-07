# dbhwrapper/__init__.py

import os
import requests

session = requests.Session()
session.data = {}

from .main import bot