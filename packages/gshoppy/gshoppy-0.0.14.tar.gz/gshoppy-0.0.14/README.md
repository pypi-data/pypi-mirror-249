## Installation

Install the package using `pip`:

`pip install gshoppy`

## Setup

You will need a [Google Cloud Platform](https://cloud.google.com/cloud-console) account and a project with the [Google Shopping API enabled](https://cloud.google.com/endpoints/docs/openapi/enable-api).
You will also need to create a [service account](https://developers.google.com/identity/protocols/oauth2/service-account) and download the credentials as a JSON file.
See [here](https://developers.google.com/shopping-content/guides/how-tos/service-accounts) for more details.

Save this file somewhere safe. You will need it to authenticate with the API.

## Usage

Import the `ProductService` class. This is the interface to the Google Shopping API.
```python
from gshoppy import ProductService
```

There is a `util` function to help you load credentials from a JSON file. This is the recommended way to load credentials.
```python
from gshoppy.utils import get_credentials_from_file
```

You will also need to use the `Product` model to create products.
```python
from gshoppy.services.models import Product
```

Tell gshoppy where to find your credentials file and load credentials with the helper function.
```python
from gshoppy.utils import get_credentials_from_file

SERVICE_ACCOUNT_FILE = "path/to/credentials.json"
credentials = get_credentials_from_file(SERVICE_ACCOUNT_FILE)
```

Create a `ProductService` instance with your credentials and merchant ID.
```python
product_service = ProductService(
    sandbox=True, # Set to False for production
    credentials=credentials,
    merchant_id="1234567890" # Your merchant ID
)
```

Use the `Product` model to create a product.
```python
import gshoppy.services.models as models

product = models.Product(
    offerId="test_product_offer_id",
    title="Test Product",
    description="Test description.",
    link="https://www.example.com",
    imageLink="https://www.example.com/image.png",
    contentLanguage="en",
    targetCountry=models.Country.US,
    channel=models.Channel.ONLINE,
    availability=models.ProductAvailability.OUT_OF_STOCK,
    price=models.Price(
        value="1.99",
        currency="USD",
    ),
    shipping=models.ProductShipping(
        country=models.Country.US,
        service="Standard shipping",
        price=models.Price(
            value="0.99",
            currency="USD",
        )
    ),
)
```

Now you can create the product in the Google Shopping API.
```python
service.insert(product)
```

You can also update a product.
```python
service.update(product.offerId, title="New title")
```

List existing products:
```python
products = service.list()
for product in products:
    print(product.offerId)
```

Delete a product:
```python
service.delete(product.offerId)
```
