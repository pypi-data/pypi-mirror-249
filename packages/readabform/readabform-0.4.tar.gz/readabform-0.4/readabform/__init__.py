to_exclude = ['readabform']
from main import *
for name in to_exclude:
    __builtins__.globals().pop(name)