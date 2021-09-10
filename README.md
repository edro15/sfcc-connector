# Salesforce Commerce Cloud connector
This library enables users to leverage a client offering resources to perform API calls against Salesforce Commerce Cloud (SFCC) via the standard [Open Commerce API (OCAPI)](https://www.salesforce.com/video/2520463/).

## Getting Started
### Installation
TODO

### Usage
TODO

### Example
```python
#!/usr/bin/env python3
from __future__ import absolute_import
from datetime import datetime, timedelta

from src.connector import SFCCCore
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
    client = SFCCCore(default_config)

    # Perform calls against SFCC
    try:
        # Authentication is required to perform other calls
        resp = client.authenticate()
        print("{}\n\n".format(resp))

        # Fetching order details for order with ID = 1
        resp = client.get_order(1)
        print("{}\n\n".format(resp))

        # Fetching all orders from yesterday up to now
        begin = datetime.now()
        end = begin - timedelta(days=1)
        resp = client.get_orders(begin, end)
        print("{}\n\n".format(resp))

        # Fetching all jobs from yesterday up to now
        resp = client.get_jobs(begin, end)
        print("{}\n\n".format(resp))
        
    except APIRequestError as e:
        print("Error {}".format(e))
```


## Contributing 
Do you want to use this library for your own projects? Great!

* Want to contribute? Even better! Feel free to create a [PR](https://github.com/edro15/sfcc-connector/pulls)
* Found a bug? [Open an issue](https://github.com/edro15/sfcc-connector/issues)

## License
MIT Licensed. See [LICENSE](LICENSE) for full details.