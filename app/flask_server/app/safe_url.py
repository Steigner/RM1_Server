# library -> standard python libary - url
from urllib.parse import urlparse, urljoin

# library -> flask - request
from flask import request


# public function:
#   input: target url
#   return: tested url -> if url is valid
# Note: parser for get information if next url is valid url for redirect, this is used for logging mainly
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
