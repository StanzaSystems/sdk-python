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


class V1GuardFeatureSelector(object):
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
        "environment": "str",
        "guard_name": "str",
        "feature_name": "str",
        "tags": "list[Hubv1Tag]",
    }

    attribute_map = {
        "environment": "environment",
        "guard_name": "guardName",
        "feature_name": "featureName",
        "tags": "tags",
    }

    def __init__(
        self,
        environment=None,
        guard_name=None,
        feature_name=None,
        tags=None,
        _configuration=None,
    ):  # noqa: E501
        """V1GuardFeatureSelector - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._environment = None
        self._guard_name = None
        self._feature_name = None
        self._tags = None
        self.discriminator = None

        self.environment = environment
        self.guard_name = guard_name
        if feature_name is not None:
            self.feature_name = feature_name
        if tags is not None:
            self.tags = tags

    @property
    def environment(self):
        """Gets the environment of this V1GuardFeatureSelector.  # noqa: E501


        :return: The environment of this V1GuardFeatureSelector.  # noqa: E501
        :rtype: str
        """
        return self._environment

    @environment.setter
    def environment(self, environment):
        """Sets the environment of this V1GuardFeatureSelector.


        :param environment: The environment of this V1GuardFeatureSelector.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and environment is None:
            raise ValueError(
                "Invalid value for `environment`, must not be `None`"
            )  # noqa: E501

        self._environment = environment

    @property
    def guard_name(self):
        """Gets the guard_name of this V1GuardFeatureSelector.  # noqa: E501


        :return: The guard_name of this V1GuardFeatureSelector.  # noqa: E501
        :rtype: str
        """
        return self._guard_name

    @guard_name.setter
    def guard_name(self, guard_name):
        """Sets the guard_name of this V1GuardFeatureSelector.


        :param guard_name: The guard_name of this V1GuardFeatureSelector.  # noqa: E501
        :type: str
        """
        if self._configuration.client_side_validation and guard_name is None:
            raise ValueError(
                "Invalid value for `guard_name`, must not be `None`"
            )  # noqa: E501

        self._guard_name = guard_name

    @property
    def feature_name(self):
        """Gets the feature_name of this V1GuardFeatureSelector.  # noqa: E501


        :return: The feature_name of this V1GuardFeatureSelector.  # noqa: E501
        :rtype: str
        """
        return self._feature_name

    @feature_name.setter
    def feature_name(self, feature_name):
        """Sets the feature_name of this V1GuardFeatureSelector.


        :param feature_name: The feature_name of this V1GuardFeatureSelector.  # noqa: E501
        :type: str
        """

        self._feature_name = feature_name

    @property
    def tags(self):
        """Gets the tags of this V1GuardFeatureSelector.  # noqa: E501


        :return: The tags of this V1GuardFeatureSelector.  # noqa: E501
        :rtype: list[Hubv1Tag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this V1GuardFeatureSelector.


        :param tags: The tags of this V1GuardFeatureSelector.  # noqa: E501
        :type: list[Hubv1Tag]
        """

        self._tags = tags

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
        if issubclass(V1GuardFeatureSelector, dict):
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
        if not isinstance(other, V1GuardFeatureSelector):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1GuardFeatureSelector):
            return True

        return self.to_dict() != other.to_dict()
