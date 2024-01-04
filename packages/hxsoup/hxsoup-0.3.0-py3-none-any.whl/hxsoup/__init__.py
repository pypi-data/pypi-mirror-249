"""HttpX + beautifulSOUP

Various convenient features related to httpx and BeautifulSoup.

██╗░░██╗██╗░░██╗░██████╗░█████╗░██╗░░░██╗██████╗░
██║░░██║╚██╗██╔╝██╔════╝██╔══██╗██║░░░██║██╔══██╗
███████║░╚███╔╝░╚█████╗░██║░░██║██║░░░██║██████╔╝
██╔══██║░██╔██╗░░╚═══██╗██║░░██║██║░░░██║██╔═══╝░
██║░░██║██╔╝╚██╗██████╔╝╚█████╔╝╚██████╔╝██║░░░░░
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░░╚════╝░░╚═════╝░╚═╝░░░░░
"""

__title__ = "hxsoup"
__description__ = "Various convenient features related to httpx and BeautifulSoup."
__version_info__ = (0, 3, 0)
__version__ = str.join(".", map(str, __version_info__))
__author__ = "ilotoki0804"
__author_email__ = "ilotoki0804@gmail.com"
__license__ = "MIT License"

__github_user_name__ = __author__
__github_project_name__ = __title__

from .api import delete, get, head, options, patch, post, put, request, stream
from .broadcast_list import BroadcastList
from .client import Client, AsyncClient, DEV_HEADERS, DEV_DEFAULT_TIMEOUT_CONFIG
from .souptools import SoupedResponse, SoupTools, Parsers
from .options import ClientOptions, MutableClientOptions
from .utils import freeze_dict_and_list, clean_headers
