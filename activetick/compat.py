
import sys

if sys.version_info >= (3, 0):
    from io import BytesIO as IO
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    import StringIO as IO
    from urllib import urlencode, urlopen
