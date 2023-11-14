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


class V1SetTokenLeaseConsumedRequest(object):
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
    swagger_types = {
        "tokens": "list[str]",
        "weight_correction": "float",
        "environment": "str",
    }

    attribute_map = {
        "tokens": "tokens",
        "weight_correction": "weightCorrection",
        "environment": "environment",
    }

    def __init__(
        self, tokens=None, weight_correction=None, environment=None, _configuration=None
    ):  # noqa: E501
        """V1SetTokenLeaseConsumedRequest - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._tokens = None
        self._weight_correction = None
        self._environment = None
        self.discriminator = None

        self.tokens = tokens
        if weight_correction is not None:
            self.weight_correction = weight_correction
        if environment is not None:
            self.environment = environment

    @property
    def tokens(self):
        """Gets the tokens of this V1SetTokenLeaseConsumedRequest.  # noqa: E501


        :return: The tokens of this V1SetTokenLeaseConsumedRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._tokens

    @tokens.setter
    def tokens(self, tokens):
        """Sets the tokens of this V1SetTokenLeaseConsumedRequest.


        :param tokens: The tokens of this V1SetTokenLeaseConsumedRequest.  # noqa: E501
        :type: list[str]
        """
        if self._configuration.client_side_validation and tokens is None:
            raise ValueError(
                "Invalid value for `tokens`, must not be `None`"
            )  # noqa: E501

        self._tokens = tokens

    @property
    def weight_correction(self):
        """Gets the weight_correction of this V1SetTokenLeaseConsumedRequest.  # noqa: E501

        Used for request weighting, i.e. accounting for varying request sizes and costs. If weights are not known before request execution, then a default or estimated weight may be used, followed by a corrected value here. If a value is sent here, it should be the actual request weight.  # noqa: E501

        :return: The weight_correction of this V1SetTokenLeaseConsumedRequest.  # noqa: E501
        :rtype: float
        """
        return self._weight_correction

    @weight_correction.setter
    def weight_correction(self, weight_correction):
        """Sets the weight_correction of this V1SetTokenLeaseConsumedRequest.

        Used for request weighting, i.e. accounting for varying request sizes and costs. If weights are not known before request execution, then a default or estimated weight may be used, followed by a corrected value here. If a value is sent here, it should be the actual request weight.  # noqa: E501

        :param weight_correction: The weight_correction of this V1SetTokenLeaseConsumedRequest.  # noqa: E501
        :type: float
        """

        self._weight_correction = weight_correction

    @property
    def environment(self):
        """Gets the environment of this V1SetTokenLeaseConsumedRequest.  # noqa: E501

        Must be specified.  # noqa: E501

        :return: The environment of this V1SetTokenLeaseConsumedRequest.  # noqa: E501
        :rtype: str
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """Sets the environment of this V1SetTokenLeaseConsumedRequest.

        Must be specified.  # noqa: E501

        :param environment: The environment of this V1SetTokenLeaseConsumedRequest.  # noqa: E501
        :type: str
        """

        self._environment = environment

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
        if issubclass(V1SetTokenLeaseConsumedRequest, dict):
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
        if not isinstance(other, V1SetTokenLeaseConsumedRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1SetTokenLeaseConsumedRequest):
            return True

        return self.to_dict() != other.to_dict()
