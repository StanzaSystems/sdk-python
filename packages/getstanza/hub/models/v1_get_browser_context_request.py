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


class V1GetBrowserContextRequest(object):
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
    swagger_types = {"feature": "V1FeatureSelector"}

    attribute_map = {"feature": "feature"}

    def __init__(self, feature=None, _configuration=None):  # noqa: E501
        """V1GetBrowserContextRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._feature = None
        self.discriminator = None

        if feature is not None:
            self.feature = feature

    @property
    def feature(self):
        """Gets the feature of this V1GetBrowserContextRequest.  # noqa: E501

        Information required to select and return the most recent BrowserContext version. If Feature names is nil, will return all Features in the organization associated with the bearer token/API key, otherwise only information related to the named Features will be returned.  # noqa: E501

        :return: The feature of this V1GetBrowserContextRequest.  # noqa: E501
        :rtype: V1FeatureSelector
        """
        return self._feature

    @feature.setter
    def feature(self, feature):
        """Sets the feature of this V1GetBrowserContextRequest.

        Information required to select and return the most recent BrowserContext version. If Feature names is nil, will return all Features in the organization associated with the bearer token/API key, otherwise only information related to the named Features will be returned.  # noqa: E501

        :param feature: The feature of this V1GetBrowserContextRequest.  # noqa: E501
        :type: V1FeatureSelector
        """

        self._feature = feature

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
        if issubclass(V1GetBrowserContextRequest, dict):
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
        if not isinstance(other, V1GetBrowserContextRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1GetBrowserContextRequest):
            return True

        return self.to_dict() != other.to_dict()
