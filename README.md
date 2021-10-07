# Salesforce Commerce Cloud connector
[![PyPI version](https://badge.fury.io/py/sfcc-connector.svg)](https://badge.fury.io/py/sfcc-connector)
![Python](https://img.shields.io/pypi/pyversions/sfcc-connector.svg)
[![Actions Status: test](https://github.com/edro15/sfcc-connector/actions/workflows/test.yml/badge.svg)](https://github.com/edro15/sfcc-connector/actions?query=workflow%3A"Python%20testing")
[![Actions Status: release](https://github.com/edro15/sfcc-connector/actions/workflows/release.yml/badge.svg)](https://github.com/edro15/sfcc-connector/actions?query=workflow%3A"Publish%20PyPI")

This package enables users to leverage a client offering resources to perform API calls against Salesforce Commerce Cloud (SFCC) via the standard [Open Commerce API (OCAPI)](https://www.salesforce.com/video/2520463/).

## Features
* Business Manager user grant authentication
* Retry policy on each call:
    * Applies to every request responding with 5xx status code
    * Max of 5 minutes with exponential backoff strategy with a max wait time of 30s 
    * Stop after 5 mins of attempts
* Limited amount of APIs offered but highly scalable and flexible model to integrate more at need

    
## Getting Started
### Installation

To install the tool via `pip` from `PyPI`:

```bash
pip install sfcc-connector
```

### Usage
#### Simple Example

```python
#!/usr/bin/env python3
from __future__ import absolute_import
from datetime import datetime, timedelta

from src.connector import SFCCClient
from apiclient.exceptions import APIRequestError


if __name__ == "__main__":
    # !! Please replace values opportunely in your configuration !!
    default_config = {
        "domain": "<YOUR-DOMAIN:YOUR-PORT>",
        "ocapi_version": "<YOUR-OCAPI-VERSION>",
        "site_id": "<YOUR-SITE-ID>",
        "use_ssl": False,
        "is_production": False,
        "username": "<YOUR_USERNAME>",
        "password": "<YOUR_PASSWORD>",
        "client_id": "<YOUR-CLIENT-ID>",
        "client_password": "<YOUR-CLIENT-PWD>"
    }

    # Initialize client
    client = SFCCClient(default_config)

    # Perform calls against SFCC
    try:
        # Authentication is required to perform other calls
        resp = client.authenticate()
        print("Authentication response: {}".format(resp))

        # Fetching order details for order with ID = 1
        resp = client.get_order(1)
        print("Get Order (1) response: {}".format(resp))

        # Fetching all orders from yesterday up to now
        end = datetime.now()
        begin = end - timedelta(days=1)
        resp = client.get_orders(begin, end)
        print("Get Orders response: {}".format(resp))

        # Fetching all jobs from yesterday up to now
        resp = client.get_jobs(begin, end)
        print("Get Jobs response: {}".format(resp))
        
    except APIRequestError as e:
        print("Error {}".format(e))
```

The `SFCCClient` exposes a number of predefined methods that can be called to access equivalent resources on Salesforce Commerce Cloud.

* [`authenticate`](https://github.com/edro15/sfcc-connector#authenticate)
* [`get_orders`](https://github.com/edro15/sfcc-connector#get_orders)
* [`get_order`](https://github.com/edro15/sfcc-connector#get_orders)
* [`get_jobs`](https://github.com/edro15/sfcc-connector#get_jobs)

#### `authenticate`
No arguments to be provided. Returns a valid token according to [specs](https://documentation.b2c.commercecloud.salesforce.com/DOC1/index.jsp?topic=%2Fcom.demandware.dochelp%2FOCAPI%2Fcurrent%2Fdata%2FResources%2FLogRequests.html&cp=0_15_4_30) when successful.

#### `get_orders`
The query used by default will retrieve all orders having `creation_date` or `last_modified` within the time interval defined by given `begin_date` and `end_date`. 
Provide another query (`custom_query`) if you want to filter orders based on other criteria.

By default all order fields will be returned. If you need to retrieve only a selection of them, please provide a `custom_select` as for example: `custom_select="(hits.(data.(creation_date,confirmation_status,total)))"`

| **Arguments**              | **Format** | **Description**                                                                                                                                                                                                                                                     |
|----------------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `begin_date`               | `datetime` | Used to filter orders based on time interval                                                                                                                                                                                                                        |
| `end_date`                 | `datetime` | Used to filter orders based on time interval                                                                                                                                                                                                                        |
| (optional)  `custom_query` | `dict`     | To be built according to [specs](https://documentation.b2c.commercecloud.salesforce.com/DOC1/index.jsp?topic=%2Fcom.demandware.dochelp%2FOCAPI%2Fcurrent%2Fshop%2FDocuments%2FOrderSearchRequest.html&anchor=id635091637)  |
| (optional) `custom_select` | `str`      | To limit the amount of returned fields |


#### `get_order`

| **Arguments** | **Format** | **Description**                           |
|---------------|------------|-------------------------------------------|
| `order`    | `int`      | Order ID to identify the order to be fetched |

#### `get_jobs`
The query used by default will retrieve all jobs having `start_time` or `end_time` within the time interval defined by given `begin_date` and `end_date`. Provide another query (`custom_query`) if you want to filter orders based on other criteria.

By default all order fields will be returned. If you need to retrieve only a selection of them, please provide an opportune `custom_select`

| **Arguments**              | **Format** | **Description**                                                                                                                                                                                                                                                     |
|----------------------------|------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `begin_date`               | `datetime` | Used to filter jobs based on time interval                                                                                                                                                                                                                        |
| `end_date`                 | `datetime` | Used to filter jobs based on time interval                                                                                                                                                                                                                        |
| (optional)  `custom_query` | `dict`     | To be built according to [specs](https://documentation.b2c.commercecloud.salesforce.com/DOC1/index.jsp?topic=%2Fcom.demandware.dochelp%2FOCAPI%2Fcurrent%2Fshop%2FDocuments%2FOrderSearchRequest.html&anchor=id635091637)  |
| (optional) `custom_select` | `str`      | To limit the amount of returned fields |


## Contributing 
Do you want to use this library for your own projects? Great!

* Want to contribute? Even better! Feel free to create a [PR](https://github.com/edro15/sfcc-connector/pulls)
* Found a bug? [Open an issue](https://github.com/edro15/sfcc-connector/issues)

## License
MIT Licensed. See [LICENSE](LICENSE) for full details.