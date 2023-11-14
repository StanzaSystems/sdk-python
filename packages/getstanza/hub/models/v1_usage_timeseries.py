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


class V1UsageTimeseries(object):
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
        "data": "list[V1UsageTSDataPoint]",
        "feature": "str",
        "priority": "int",
        "tags": "list[Hubv1Tag]",
        "guard": "str",
        "service": "str",
    }

    attribute_map = {
        "data": "data",
        "feature": "feature",
        "priority": "priority",
        "tags": "tags",
        "guard": "guard",
        "service": "service",
    }

    def __init__(
        self,
        data=None,
        feature=None,
        priority=None,
        tags=None,
        guard=None,
        service=None,
        _configuration=None,
    ):  # noqa: E501
        """V1UsageTimeseries - a model defined in Swagger"""  # noqa: E501
        if _configuration is None:
            _configuration = Configuration()
        self._configuration = _configuration

        self._data = None
        self._feature = None
        self._priority = None
        self._tags = None
        self._guard = None
        self._service = None
        self.discriminator = None

        if data is not None:
            self.data = data
        if feature is not None:
            self.feature = feature
        if priority is not None:
            self.priority = priority
        if tags is not None:
            self.tags = tags
        if guard is not None:
            self.guard = guard
        if service is not None:
            self.service = service

    @property
    def data(self):
        """Gets the data of this V1UsageTimeseries.  # noqa: E501


        :return: The data of this V1UsageTimeseries.  # noqa: E501
        :rtype: list[V1UsageTSDataPoint]
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this V1UsageTimeseries.


        :param data: The data of this V1UsageTimeseries.  # noqa: E501
        :type: list[V1UsageTSDataPoint]
        """

        self._data = data

    @property
    def feature(self):
        """Gets the feature of this V1UsageTimeseries.  # noqa: E501


        :return: The feature of this V1UsageTimeseries.  # noqa: E501
        :rtype: str
        """
        return self._feature

    @feature.setter
    def feature(self, feature):
        """Sets the feature of this V1UsageTimeseries.


        :param feature: The feature of this V1UsageTimeseries.  # noqa: E501
        :type: str
        """

        self._feature = feature

    @property
    def priority(self):
        """Gets the priority of this V1UsageTimeseries.  # noqa: E501


        :return: The priority of this V1UsageTimeseries.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this V1UsageTimeseries.


        :param priority: The priority of this V1UsageTimeseries.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def tags(self):
        """Gets the tags of this V1UsageTimeseries.  # noqa: E501


        :return: The tags of this V1UsageTimeseries.  # noqa: E501
        :rtype: list[Hubv1Tag]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this V1UsageTimeseries.


        :param tags: The tags of this V1UsageTimeseries.  # noqa: E501
        :type: list[Hubv1Tag]
        """

        self._tags = tags

    @property
    def guard(self):
        """Gets the guard of this V1UsageTimeseries.  # noqa: E501


        :return: The guard of this V1UsageTimeseries.  # noqa: E501
        :rtype: str
        """
        return self._guard

    @guard.setter
    def guard(self, guard):
        """Sets the guard of this V1UsageTimeseries.


        :param guard: The guard of this V1UsageTimeseries.  # noqa: E501
        :type: str
        """

        self._guard = guard

    @property
    def service(self):
        """Gets the service of this V1UsageTimeseries.  # noqa: E501


        :return: The service of this V1UsageTimeseries.  # noqa: E501
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service):
        """Sets the service of this V1UsageTimeseries.


        :param service: The service of this V1UsageTimeseries.  # noqa: E501
        :type: str
        """

        self._service = service

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
        if issubclass(V1UsageTimeseries, dict):
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
        if not isinstance(other, V1UsageTimeseries):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, V1UsageTimeseries):
            return True

        return self.to_dict() != other.to_dict()