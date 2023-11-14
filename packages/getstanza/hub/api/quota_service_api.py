# coding: utf-8

"""
    Stanza Hub API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: support@stanza.systems
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six
from getstanza.hub.api_client import ApiClient


class QuotaServiceApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def quota_service_get_token(self, body, **kwargs):  # noqa: E501
        """Get Access Token  # noqa: E501

        Get a single token from Stanza Hub for access to given Guard (optional Feature name for priority).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_get_token(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1GetTokenRequest body: Requests token for given Guard at priority of specified feature. (required)
        :return: V1GetTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.quota_service_get_token_with_http_info(
                body, **kwargs
            )  # noqa: E501
        else:
            (data) = self.quota_service_get_token_with_http_info(
                body, **kwargs
            )  # noqa: E501
            return data

    def quota_service_get_token_with_http_info(self, body, **kwargs):  # noqa: E501
        """Get Access Token  # noqa: E501

        Get a single token from Stanza Hub for access to given Guard (optional Feature name for priority).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_get_token_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1GetTokenRequest body: Requests token for given Guard at priority of specified feature. (required)
        :return: V1GetTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ["body"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quota_service_get_token" % key
                )
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if self.api_client.client_side_validation and (
            "body" not in params or params["body"] is None
        ):  # noqa: E501
            raise ValueError(
                "Missing the required parameter `body` when calling `quota_service_get_token`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "body" in params:
            body_params = params["body"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # HTTP header `Content-Type`
        header_params[
            "Content-Type"
        ] = self.api_client.select_header_content_type(  # noqa: E501
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth"]  # noqa: E501

        return self.api_client.call_api(
            "/v1/quota/token",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="V1GetTokenResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def quota_service_get_token_lease(self, body, **kwargs):  # noqa: E501
        """Get Access Token Leases  # noqa: E501

        Get a set of token leases from Stanza Hub for access to given Guard (optional Feature name for priority).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_get_token_lease(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1GetTokenLeaseRequest body: Requests token lease for given Guard at priority of specified feature. (required)
        :return: V1GetTokenLeaseResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.quota_service_get_token_lease_with_http_info(
                body, **kwargs
            )  # noqa: E501
        else:
            (data) = self.quota_service_get_token_lease_with_http_info(
                body, **kwargs
            )  # noqa: E501
            return data

    def quota_service_get_token_lease_with_http_info(
        self, body, **kwargs
    ):  # noqa: E501
        """Get Access Token Leases  # noqa: E501

        Get a set of token leases from Stanza Hub for access to given Guard (optional Feature name for priority).  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_get_token_lease_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1GetTokenLeaseRequest body: Requests token lease for given Guard at priority of specified feature. (required)
        :return: V1GetTokenLeaseResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ["body"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quota_service_get_token_lease" % key
                )
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if self.api_client.client_side_validation and (
            "body" not in params or params["body"] is None
        ):  # noqa: E501
            raise ValueError(
                "Missing the required parameter `body` when calling `quota_service_get_token_lease`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "body" in params:
            body_params = params["body"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # HTTP header `Content-Type`
        header_params[
            "Content-Type"
        ] = self.api_client.select_header_content_type(  # noqa: E501
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth"]  # noqa: E501

        return self.api_client.call_api(
            "/v1/quota/lease",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="V1GetTokenLeaseResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def quota_service_set_token_lease_consumed(self, body, **kwargs):  # noqa: E501
        """Consume Access Tokens  # noqa: E501

        Inform Stanza Hub that quota access tokens were consumed.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_set_token_lease_consumed(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1SetTokenLeaseConsumedRequest body: Notifies Hub that one or more token leases has been used, i.e. Guard has been exercised. (required)
        :return: V1SetTokenLeaseConsumedResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.quota_service_set_token_lease_consumed_with_http_info(
                body, **kwargs
            )  # noqa: E501
        else:
            (data) = self.quota_service_set_token_lease_consumed_with_http_info(
                body, **kwargs
            )  # noqa: E501
            return data

    def quota_service_set_token_lease_consumed_with_http_info(
        self, body, **kwargs
    ):  # noqa: E501
        """Consume Access Tokens  # noqa: E501

        Inform Stanza Hub that quota access tokens were consumed.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_set_token_lease_consumed_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1SetTokenLeaseConsumedRequest body: Notifies Hub that one or more token leases has been used, i.e. Guard has been exercised. (required)
        :return: V1SetTokenLeaseConsumedResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ["body"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quota_service_set_token_lease_consumed" % key
                )
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if self.api_client.client_side_validation and (
            "body" not in params or params["body"] is None
        ):  # noqa: E501
            raise ValueError(
                "Missing the required parameter `body` when calling `quota_service_set_token_lease_consumed`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "body" in params:
            body_params = params["body"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # HTTP header `Content-Type`
        header_params[
            "Content-Type"
        ] = self.api_client.select_header_content_type(  # noqa: E501
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth"]  # noqa: E501

        return self.api_client.call_api(
            "/v1/quota/consumed",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="V1SetTokenLeaseConsumedResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def quota_service_validate_token(self, body, **kwargs):  # noqa: E501
        """Validate Access Tokens  # noqa: E501

        Validate quota access tokens with Stanza Hub.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_validate_token(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1ValidateTokenRequest body: Calls Hub to validate a token (ensures token has not expired, was minted by Hub, and related to the specified Guard). Used from Ingress Guards. Ensures callers have acquired quota prior to expending resources. (required)
        :return: V1ValidateTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        if kwargs.get("async_req"):
            return self.quota_service_validate_token_with_http_info(
                body, **kwargs
            )  # noqa: E501
        else:
            (data) = self.quota_service_validate_token_with_http_info(
                body, **kwargs
            )  # noqa: E501
            return data

    def quota_service_validate_token_with_http_info(self, body, **kwargs):  # noqa: E501
        """Validate Access Tokens  # noqa: E501

        Validate quota access tokens with Stanza Hub.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.quota_service_validate_token_with_http_info(body, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param V1ValidateTokenRequest body: Calls Hub to validate a token (ensures token has not expired, was minted by Hub, and related to the specified Guard). Used from Ingress Guards. Ensures callers have acquired quota prior to expending resources. (required)
        :return: V1ValidateTokenResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ["body"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        params = locals()
        for key, val in six.iteritems(params["kwargs"]):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method quota_service_validate_token" % key
                )
            params[key] = val
        del params["kwargs"]
        # verify the required parameter 'body' is set
        if self.api_client.client_side_validation and (
            "body" not in params or params["body"] is None
        ):  # noqa: E501
            raise ValueError(
                "Missing the required parameter `body` when calling `quota_service_validate_token`"
            )  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "body" in params:
            body_params = params["body"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(
            ["application/json"]
        )  # noqa: E501

        # HTTP header `Content-Type`
        header_params[
            "Content-Type"
        ] = self.api_client.select_header_content_type(  # noqa: E501
            ["application/json"]
        )  # noqa: E501

        # Authentication setting
        auth_settings = ["ApiKeyAuth"]  # noqa: E501

        return self.api_client.call_api(
            "/v1/quota/validatetokens",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="V1ValidateTokenResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get("async_req"),
            _return_http_data_only=params.get("_return_http_data_only"),
            _preload_content=params.get("_preload_content", True),
            _request_timeout=params.get("_request_timeout"),
            collection_formats=collection_formats,
        )