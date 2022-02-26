# Add to path
from sys import path
import os
path.insert(0, os.path.join(os.getcwd(), '../../'))

# Database handler
from __init__ import DB
