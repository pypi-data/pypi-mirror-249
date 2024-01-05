from .error import (  # noqa: F401
    APIConnectionError,
    APIError,
    BookNotFoundError,
    DibukError,
)
from .resource import Book, Catalogue, Category, Order  # noqa: F401

# Configuration variables
api_credentials = None

DIBUK_API_VERSION = "2.3"
DIBUK_API_ENDPOINT = "https://agregator.dibuk.eu/2_3/call.php"
