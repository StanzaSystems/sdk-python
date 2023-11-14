# coding: utf-8

"""
    Stanza Hub API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: support@stanza.systems
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six
from getstanza.hub.configuration import Configuration


class V1GetBearerTokenResponse(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {"bearer_token": "str"}

    attribute_map = {"bearer_token": "bearerToken"}

    def __init__(self, bearer_token=None, _configuration=None):  # noqa: E501
        """V1GetBearerTokenResponse - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._bearer_token = None
        self.discriminator = None

        if bearer_token is not None:
            self.bearer_token = bearer_token

    @property
    def bearer_token(self):
        """Gets the bearer_token of this V1GetBearerTokenResponse.  # noqa: E501


        :return: The bearer_token of this V1GetBearerTokenResponse.  # noqa: E501
        :rtype: str
        """
        return self._bearer_token

    @bearer_token.setter
    def bearer_token(self, bearer_token):
        """Sets the bearer_token of this V1GetBearerTokenResponse.


        :param bearer_token: The bearer_token of this V1GetBearerTokenResponse.  # noqa: E501
        :type: str
        """

        self._bearer_token = bearer_token

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(V1GetBearerTokenResponse, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1GetBearerTokenResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1GetBearerTokenResponse):
            return True

        return self.to_dict() != other.to_dict()