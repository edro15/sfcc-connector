import inspect
from datetime import datetime
from apiclient import (
    APIClient,
    paginated,
    retry_request
)

from sfcc_connector import api
from sfcc_connector.api import *

from .queries import default_query


def get_next_page(response, previous_page_params):
    return {
        "count": response["count"],
        "start": response["start"] + response["count"]
    }


# Extend the client for your API integration.
class APIConnector(APIClient):
    """ Definition of client integrating with
        SFCC via OCAPI.
    """

    def __init__(self, **args):
        if "config" in args.keys():
            # Setting up configuration
            cfg = args.pop("config")
            Endpoint.config = cfg

        super().__init__(**args)

        # Configuring all available endpoints
        endpoints = dict([(name, cls) for name, cls in api.__dict__.items() if isinstance(cls, type)])
        for key, endpoint in endpoints.items():
            # print("Entering endpoint {}".format(key))
            if key.endswith("Endpoint") and key != "Endpoint":
                # e.g. objs are as such 'Endpoint': <class 'src.connector.api.api.Endpoint'>
                cfg = Endpoint.config
                ocapi_v = cfg.ocapi_version
                base_url = cfg.base_url
                domain = cfg.base_domain
                site_id = cfg.site_id

                for name, value in inspect.getmembers(endpoint):
                    if name.startswith("_") or inspect.ismethod(value) or inspect.isfunction(value):
                        # Ignore any private or class attributes.
                        continue
                    new_value = str(value).lstrip("/")
                    # TODO consider using Template
                    resource = new_value.replace("{url}", base_url) \
                                        .replace("{ocapi_version}", ocapi_v) \
                                        .replace("{domain}", domain)
                    # FIXME ?
                    if key.startswith("Data"):
                        resource = resource.replace(site_id, "-")
                    setattr(endpoint, name, resource)

    @retry_request
    def authenticate(self) -> dict:
        """ Perform authentication at SFCC. When successful, returns valid token.

            Retry policy:
            * Every request responding w/ 5xx status code
            * Max of 5 minutes with exponential backoff strategy with a maximum wait time of 30 seconds.
            * Retrying will stop after 5 minutes
        """

        grant_type = {
            "grant_type": "urn:demandware:params:oauth:grant-type:client-id:dwsid:dwsecuretoken"
        }

        return self.post(AuthEndpoint.access_token.format(client_id=Endpoint.config.client_id), grant_type)

    @paginated(by_query_params=get_next_page)
    @retry_request
    def get_orders(self, begin_date: datetime, end_date: datetime, custom_query=dict(), custom_select=str()) -> dict:
        dt_format = "%Y-%m-%dT%H:%M:%S.000Z"

        if custom_query:
            query = custom_query

        else:
            query = default_query
            range_filters = [{
                "range_filter": {
                    "field": "creation_date",
                    "from": "{}".format(begin_date.strftime(dt_format)),
                    "to": "{}".format(end_date.strftime(dt_format))
                }
            }, {
                "range_filter": {
                    "field": "last_modified",
                    "from": "{}".format(begin_date.strftime(dt_format)),
                    "to": "{}".format(end_date.strftime(dt_format))
                }
            }]

            query["sorts"] = [{
                "field": "order_no",
                "sort_order": "asc"
            }]

            query["query"]["filtered_query"]["filter"]["bool_filter"]["filters"] = range_filters

        # To reduce amount of info retrieved at SFCC, use select as shown below
        if custom_select:
            query["select"] = custom_select
            # query["select"] = "(count,total,start,hits.(data.(order_no,creation_date)))"

        return self.post(ShopEndpoint.order_search, query)

    @retry_request
    def get_order(self, order: int) -> dict:
        return self.get(ShopEndpoint.order.format(order_no=order))

    @paginated(by_query_params=get_next_page)
    @retry_request
    def get_jobs(self, begin_date: datetime, end_date: datetime, custom_query=dict(), custom_select=str()) -> dict:
        dt_format = "%Y-%m-%dT%H:%M:%S.000Z"

        if custom_query:
            query = custom_query

        else:
            query = default_query
            range_filters = [{
                "range_filter": {
                    "field": "start_time",
                    "from": "{}".format(begin_date.strftime(dt_format)),
                    "to": "{}".format(end_date.strftime(dt_format))
                }
            }, {
                "range_filter": {
                    "field": "end_time",
                    "from": "{}".format(begin_date.strftime(dt_format)),
                    "to": "{}".format(end_date.strftime(dt_format))
                }
            }]

            query["sorts"] = [{
                "field": "id",
                "sort_order": "asc"
            }]

            query["query"]["filtered_query"]["filter"]["bool_filter"]["filters"] = range_filters

        if custom_select:
            query["select"] = custom_select

        return self.post(DataEndpoint.job_execution_search, query)

    #
    # Add here other API calls
    #
