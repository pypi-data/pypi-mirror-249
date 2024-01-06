from .response import Response, ProcessResponse
from .session import Session, TLSSession, chrome, firefox
from .reqs import *
from .headers import Headers

# attempt to import headless browsing dependencies
try:
    from .playwright_mock import ChromeBrowser, FirefoxBrowser
    from .browser import BrowserSession, render
except ModuleNotFoundError:
    import os
    from sys import stderr

    # give windows users a warning
    os.name == 'nt' and stderr.write(
        'WARNING: Please run `pip install playfulrequests[all]` for headless browsing support.\n'
    )

from .parser import HTML
from .__version__ import __version__
from .__version__ import __author__
