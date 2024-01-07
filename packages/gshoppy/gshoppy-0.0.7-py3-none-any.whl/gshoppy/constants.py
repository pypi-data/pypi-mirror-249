"""
constants.py contains constants used throughout the application.
"""
#: The application name for Google Content.
APPLICATION_NAME = "Content API for Shopping"

# The product details are provided in English.
CONTENT_LANGUAGE = "en"

# The products are sold in the USA.
TARGET_COUNTRY = "US"

# The products will be sold online.
CHANNEL = "online"

#: Service account API key file.
#: If credentials are not passed in to the service,
#: it will default to the file at this path.
SERVICE_ACCOUNT_FILE = "../credentials/charged-curve-410406-b9ed7ae95369.json"

#: The API URI.
API_URI = "https://www.googleapis.com/discovery/v1/apis/content/v2.1/rest"

#: The content scope.
CONTENT_API_SCOPE = "https://www.googleapis.com/auth/content"

#: The service name.
SERVICE_NAME = "content"

#: The service version.
SERVICE_VERSION = "v2.1"

#: The sandbox service version.
SANDBOX_SERVICE_VERSION = "v2.1sandbox"

#: The merchant ID.
# If your merchant ID is not passed in to the service,
# it will default to this value.
MERCHANT_ID = "5321244390"

#: The maximum page size.
MAX_PAGE_SIZE = 50

#: The default batch size.
#: Google's maximum is 1000
#: https://developers.google.com/shopping-content/v2/how-tos/batch
BATCH_SIZE = 1000

# Product Availability - In Stock
AVAILABILITY_IN_STOCK = "in stock"

# Product Availability - Out of Stock
AVAILABILITY_OUT_OF_STOCK = "out of stock"

# Product Availability - Preorder
AVAILABILITY_PREORDER = "preorder"
