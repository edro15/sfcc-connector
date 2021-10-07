from apiclient import endpoint
# from string import Template


class Endpoint:
    def __setattr__(self, name, value):
        self.__dict__[name] = value

#
# Define endpoints, using the provided decorator.
#


@endpoint(base_url="{domain}/dw/oauth2")
class AuthEndpoint(Endpoint):
    access_token = "access_token?client_id={client_id}"


@endpoint(base_url="{url}/shop/{ocapi_version}")
class ShopEndpoint(Endpoint):
    order_search = "order_search"
    order = "orders/{order_no}"
    #
    # Add more endpoints below
    #


@endpoint(base_url="{url}/data/{ocapi_version}")
class DataEndpoint(Endpoint):
    job_execution_search = "job_execution_search"
    #
    # Add more endpoints below
    #


@endpoint(base_url="{url}/meta/v1")
class MetadataEndpoint(Endpoint):
    list_apis = "rest"
    list_versions = "rest/data"
    list_resource_descr = "rest/data/{version}"
    list_docs = "rest/data/{version}/documents"
    get_doc_info = "rest/data/{version}/documents/{doc_id}"
