import sys

if sys.version_info < (3, 6):
    raise RuntimeError("YunTemp strongly prefers Python 3.6+")
