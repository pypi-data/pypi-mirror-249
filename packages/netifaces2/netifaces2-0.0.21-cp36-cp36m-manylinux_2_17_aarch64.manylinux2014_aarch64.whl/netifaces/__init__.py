from .netifaces import *

__doc__ = netifaces.__doc__
if hasattr(netifaces, "__all__"):
    __all__ = netifaces.__all__