
import sys

PY3 = sys.version_info >= (3, 0)

if PY3:
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib import urlencode, urlopen