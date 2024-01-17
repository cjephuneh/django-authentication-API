import os

try:
    if os.environ.get("DEBUG") == "False":
        from .production import *
    else:
        from .development import *
except ImportError:
    raise ImportError
