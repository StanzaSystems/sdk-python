#!/usr/bin/env python3
# Automatically generated file by swagger_to. DO NOT EDIT OR APPEND ANYTHING!
"""Implements the client for UsageService."""

# pylint: skip-file
# pydocstyle: add-ignore=D105,D107,D401

import contextlib
import json
from typing import Any, BinaryIO, Dict, List, MutableMapping, Optional, cast

import requests
import requests.auth


def from_obj(obj: Any, expected: List[type], path: str = "") -> Any:
    """
    Checks and converts the given obj along the expected types.

    :param obj: to be converted
    :param expected: list of types representing the (nested) structure
    :param path: to the object used for debugging
    :return: the converted object
    """
    if not expected:
        raise ValueError(
            "`expected` is empty, but at least one type needs to be specified."
        )

    exp = expected[0]

    if exp == float:
        if isinstance(obj, int):
            return float(obj)

        if isinstance(obj, float):
            return obj

        raise ValueError(
            "Expected object of type int or float at {!r}, but got {}.".format(
                path, type(obj)
            )
        )

    if exp in [bool, int, str, list, dict]:
        if not isinstance(obj, exp):
            raise ValueError(
                "Expected object of type {} at {!r}, but got {}.".format(
                    exp, path, type(obj)
                )
            )

    if exp in [bool, int, float, str]:
        return obj

    if exp == list:
        lst = []  # type: List[Any]
        for i, value in enumerate(obj):
            lst.append(
                from_obj(value, expected=expected[1:], path="{}[{}]".format(path, i))
            )

        return lst

    if exp == dict:
        adict = dict()  # type: Dict[str, Any]
        for key, value in obj.items():
            if not isinstance(key, str):
                raise ValueError(
                    "Expected a key of type str at path {!r}, got: {}".format(
                        path, type(key)
                    )
                )

            adict[key] = from_obj(
                value, expected=expected[1:], path="{}[{!r}]".format(path, key)
            )

        return adict

    if exp == Hubv1Tag:
        return hubv1_tag_from_obj(obj, path=path)

    if exp == RpcStatus:
        return rpc_status_from_obj(obj, path=path)

    if exp == V1BrowserConfig:
        return v1_browser_config_from_obj(obj, path=path)

    if exp == V1FeatureConfig:
        return v1_feature_config_from_obj(obj, path=path)

    if exp == V1FeatureSelector:
        return v1_feature_selector_from_obj(obj, path=path)

    if exp == V1GetBearerTokenResponse:
        return v1_get_bearer_token_response_from_obj(obj, path=path)

    if exp == V1GetBrowserContextRequest:
        return v1_get_browser_context_request_from_obj(obj, path=path)

    if exp == V1GetBrowserContextResponse:
        return v1_get_browser_context_response_from_obj(obj, path=path)

    if exp == V1GetGuardConfigRequest:
        return v1_get_guard_config_request_from_obj(obj, path=path)

    if exp == V1GetGuardConfigResponse:
        return v1_get_guard_config_response_from_obj(obj, path=path)

    if exp == V1GetServiceConfigRequest:
        return v1_get_service_config_request_from_obj(obj, path=path)

    if exp == V1GetServiceConfigResponse:
        return v1_get_service_config_response_from_obj(obj, path=path)

    if exp == V1GetTokenLeaseRequest:
        return v1_get_token_lease_request_from_obj(obj, path=path)

    if exp == V1GetTokenLeaseResponse:
        return v1_get_token_lease_response_from_obj(obj, path=path)

    if exp == V1GetTokenRequest:
        return v1_get_token_request_from_obj(obj, path=path)

    if exp == V1GetTokenResponse:
        return v1_get_token_response_from_obj(obj, path=path)

    if exp == V1GetUsageRequest:
        return v1_get_usage_request_from_obj(obj, path=path)

    if exp == V1GetUsageResponse:
        return v1_get_usage_response_from_obj(obj, path=path)

    if exp == V1GuardConfig:
        return v1_guard_config_from_obj(obj, path=path)

    if exp == V1GuardFeatureSelector:
        return v1_guard_feature_selector_from_obj(obj, path=path)

    if exp == V1GuardSelector:
        return v1_guard_selector_from_obj(obj, path=path)

    if exp == V1GuardServiceSelector:
        return v1_guard_service_selector_from_obj(obj, path=path)

    if exp == V1HeaderTraceConfig:
        return v1_header_trace_config_from_obj(obj, path=path)

    if exp == V1MetricConfig:
        return v1_metric_config_from_obj(obj, path=path)

    if exp == V1ParamTraceConfig:
        return v1_param_trace_config_from_obj(obj, path=path)

    if exp == V1QueryGuardHealthRequest:
        return v1_query_guard_health_request_from_obj(obj, path=path)

    if exp == V1QueryGuardHealthResponse:
        return v1_query_guard_health_response_from_obj(obj, path=path)

    if exp == V1SentinelConfig:
        return v1_sentinel_config_from_obj(obj, path=path)

    if exp == V1ServiceConfig:
        return v1_service_config_from_obj(obj, path=path)

    if exp == V1ServiceSelector:
        return v1_service_selector_from_obj(obj, path=path)

    if exp == V1SetTokenLeaseConsumedRequest:
        return v1_set_token_lease_consumed_request_from_obj(obj, path=path)

    if exp == V1SetTokenLeaseConsumedResponse:
        return v1_set_token_lease_consumed_response_from_obj(obj, path=path)

    if exp == V1SpanSelector:
        return v1_span_selector_from_obj(obj, path=path)

    if exp == V1StreamRequest:
        return v1_stream_request_from_obj(obj, path=path)

    if exp == V1StreamResult:
        return v1_stream_result_from_obj(obj, path=path)

    if exp == V1TokenInfo:
        return v1_token_info_from_obj(obj, path=path)

    if exp == V1TokenLease:
        return v1_token_lease_from_obj(obj, path=path)

    if exp == V1TokenValid:
        return v1_token_valid_from_obj(obj, path=path)

    if exp == V1TraceConfig:
        return v1_trace_config_from_obj(obj, path=path)

    if exp == V1TraceConfigOverride:
        return v1_trace_config_override_from_obj(obj, path=path)

    if exp == V1UpdateStreamsRequest:
        return v1_update_streams_request_from_obj(obj, path=path)

    if exp == V1UpdateStreamsResponse:
        return v1_update_streams_response_from_obj(obj, path=path)

    if exp == V1UsageTSDataPoint:
        return v1_usage_t_s_data_point_from_obj(obj, path=path)

    if exp == V1UsageTimeseries:
        return v1_usage_timeseries_from_obj(obj, path=path)

    if exp == V1ValidateTokenRequest:
        return v1_validate_token_request_from_obj(obj, path=path)

    if exp == V1ValidateTokenResponse:
        return v1_validate_token_response_from_obj(obj, path=path)

    raise ValueError("Unexpected `expected` type: {}".format(exp))


def to_jsonable(obj: Any, expected: List[type], path: str = "") -> Any:
    """
    Checks and converts the given object along the expected types to a JSON-able representation.

    :param obj: to be converted
    :param expected: list of types representing the (nested) structure
    :param path: path to the object used for debugging
    :return: JSON-able representation of the object
    """
    if not expected:
        raise ValueError(
            "`expected` is empty, but at least one type needs to be specified."
        )

    exp = expected[0]
    if not isinstance(obj, exp):
        raise ValueError(
            "Expected object of type {} at path {!r}, but got {}.".format(
                exp, path, type(obj)
            )
        )

    # Assert on primitive types to help type-hinting.
    if exp == bool:
        assert isinstance(obj, bool)
        return obj

    if exp == int:
        assert isinstance(obj, int)
        return obj

    if exp == float:
        assert isinstance(obj, float)
        return obj

    if exp == str:
        assert isinstance(obj, str)
        return obj

    if exp == list:
        assert isinstance(obj, list)

        lst = []  # type: List[Any]
        for i, value in enumerate(obj):
            lst.append(
                to_jsonable(value, expected=expected[1:], path="{}[{}]".format(path, i))
            )

        return lst

    if exp == dict:
        assert isinstance(obj, dict)

        adict = dict()  # type: Dict[str, Any]
        for key, value in obj.items():
            if not isinstance(key, str):
                raise ValueError(
                    "Expected a key of type str at path {!r}, got: {}".format(
                        path, type(key)
                    )
                )

            adict[key] = to_jsonable(
                value, expected=expected[1:], path="{}[{!r}]".format(path, key)
            )

        return adict

    if exp == Hubv1Tag:
        assert isinstance(obj, Hubv1Tag)
        return hubv1_tag_to_jsonable(obj, path=path)

    if exp == RpcStatus:
        assert isinstance(obj, RpcStatus)
        return rpc_status_to_jsonable(obj, path=path)

    if exp == V1BrowserConfig:
        assert isinstance(obj, V1BrowserConfig)
        return v1_browser_config_to_jsonable(obj, path=path)

    if exp == V1FeatureConfig:
        assert isinstance(obj, V1FeatureConfig)
        return v1_feature_config_to_jsonable(obj, path=path)

    if exp == V1FeatureSelector:
        assert isinstance(obj, V1FeatureSelector)
        return v1_feature_selector_to_jsonable(obj, path=path)

    if exp == V1GetBearerTokenResponse:
        assert isinstance(obj, V1GetBearerTokenResponse)
        return v1_get_bearer_token_response_to_jsonable(obj, path=path)

    if exp == V1GetBrowserContextRequest:
        assert isinstance(obj, V1GetBrowserContextRequest)
        return v1_get_browser_context_request_to_jsonable(obj, path=path)

    if exp == V1GetBrowserContextResponse:
        assert isinstance(obj, V1GetBrowserContextResponse)
        return v1_get_browser_context_response_to_jsonable(obj, path=path)

    if exp == V1GetGuardConfigRequest:
        assert isinstance(obj, V1GetGuardConfigRequest)
        return v1_get_guard_config_request_to_jsonable(obj, path=path)

    if exp == V1GetGuardConfigResponse:
        assert isinstance(obj, V1GetGuardConfigResponse)
        return v1_get_guard_config_response_to_jsonable(obj, path=path)

    if exp == V1GetServiceConfigRequest:
        assert isinstance(obj, V1GetServiceConfigRequest)
        return v1_get_service_config_request_to_jsonable(obj, path=path)

    if exp == V1GetServiceConfigResponse:
        assert isinstance(obj, V1GetServiceConfigResponse)
        return v1_get_service_config_response_to_jsonable(obj, path=path)

    if exp == V1GetTokenLeaseRequest:
        assert isinstance(obj, V1GetTokenLeaseRequest)
        return v1_get_token_lease_request_to_jsonable(obj, path=path)

    if exp == V1GetTokenLeaseResponse:
        assert isinstance(obj, V1GetTokenLeaseResponse)
        return v1_get_token_lease_response_to_jsonable(obj, path=path)

    if exp == V1GetTokenRequest:
        assert isinstance(obj, V1GetTokenRequest)
        return v1_get_token_request_to_jsonable(obj, path=path)

    if exp == V1GetTokenResponse:
        assert isinstance(obj, V1GetTokenResponse)
        return v1_get_token_response_to_jsonable(obj, path=path)

    if exp == V1GetUsageRequest:
        assert isinstance(obj, V1GetUsageRequest)
        return v1_get_usage_request_to_jsonable(obj, path=path)

    if exp == V1GetUsageResponse:
        assert isinstance(obj, V1GetUsageResponse)
        return v1_get_usage_response_to_jsonable(obj, path=path)

    if exp == V1GuardConfig:
        assert isinstance(obj, V1GuardConfig)
        return v1_guard_config_to_jsonable(obj, path=path)

    if exp == V1GuardFeatureSelector:
        assert isinstance(obj, V1GuardFeatureSelector)
        return v1_guard_feature_selector_to_jsonable(obj, path=path)

    if exp == V1GuardSelector:
        assert isinstance(obj, V1GuardSelector)
        return v1_guard_selector_to_jsonable(obj, path=path)

    if exp == V1GuardServiceSelector:
        assert isinstance(obj, V1GuardServiceSelector)
        return v1_guard_service_selector_to_jsonable(obj, path=path)

    if exp == V1HeaderTraceConfig:
        assert isinstance(obj, V1HeaderTraceConfig)
        return v1_header_trace_config_to_jsonable(obj, path=path)

    if exp == V1MetricConfig:
        assert isinstance(obj, V1MetricConfig)
        return v1_metric_config_to_jsonable(obj, path=path)

    if exp == V1ParamTraceConfig:
        assert isinstance(obj, V1ParamTraceConfig)
        return v1_param_trace_config_to_jsonable(obj, path=path)

    if exp == V1QueryGuardHealthRequest:
        assert isinstance(obj, V1QueryGuardHealthRequest)
        return v1_query_guard_health_request_to_jsonable(obj, path=path)

    if exp == V1QueryGuardHealthResponse:
        assert isinstance(obj, V1QueryGuardHealthResponse)
        return v1_query_guard_health_response_to_jsonable(obj, path=path)

    if exp == V1SentinelConfig:
        assert isinstance(obj, V1SentinelConfig)
        return v1_sentinel_config_to_jsonable(obj, path=path)

    if exp == V1ServiceConfig:
        assert isinstance(obj, V1ServiceConfig)
        return v1_service_config_to_jsonable(obj, path=path)

    if exp == V1ServiceSelector:
        assert isinstance(obj, V1ServiceSelector)
        return v1_service_selector_to_jsonable(obj, path=path)

    if exp == V1SetTokenLeaseConsumedRequest:
        assert isinstance(obj, V1SetTokenLeaseConsumedRequest)
        return v1_set_token_lease_consumed_request_to_jsonable(obj, path=path)

    if exp == V1SetTokenLeaseConsumedResponse:
        assert isinstance(obj, V1SetTokenLeaseConsumedResponse)
        return v1_set_token_lease_consumed_response_to_jsonable(obj, path=path)

    if exp == V1SpanSelector:
        assert isinstance(obj, V1SpanSelector)
        return v1_span_selector_to_jsonable(obj, path=path)

    if exp == V1StreamRequest:
        assert isinstance(obj, V1StreamRequest)
        return v1_stream_request_to_jsonable(obj, path=path)

    if exp == V1StreamResult:
        assert isinstance(obj, V1StreamResult)
        return v1_stream_result_to_jsonable(obj, path=path)

    if exp == V1TokenInfo:
        assert isinstance(obj, V1TokenInfo)
        return v1_token_info_to_jsonable(obj, path=path)

    if exp == V1TokenLease:
        assert isinstance(obj, V1TokenLease)
        return v1_token_lease_to_jsonable(obj, path=path)

    if exp == V1TokenValid:
        assert isinstance(obj, V1TokenValid)
        return v1_token_valid_to_jsonable(obj, path=path)

    if exp == V1TraceConfig:
        assert isinstance(obj, V1TraceConfig)
        return v1_trace_config_to_jsonable(obj, path=path)

    if exp == V1TraceConfigOverride:
        assert isinstance(obj, V1TraceConfigOverride)
        return v1_trace_config_override_to_jsonable(obj, path=path)

    if exp == V1UpdateStreamsRequest:
        assert isinstance(obj, V1UpdateStreamsRequest)
        return v1_update_streams_request_to_jsonable(obj, path=path)

    if exp == V1UpdateStreamsResponse:
        assert isinstance(obj, V1UpdateStreamsResponse)
        return v1_update_streams_response_to_jsonable(obj, path=path)

    if exp == V1UsageTSDataPoint:
        assert isinstance(obj, V1UsageTSDataPoint)
        return v1_usage_t_s_data_point_to_jsonable(obj, path=path)

    if exp == V1UsageTimeseries:
        assert isinstance(obj, V1UsageTimeseries)
        return v1_usage_timeseries_to_jsonable(obj, path=path)

    if exp == V1ValidateTokenRequest:
        assert isinstance(obj, V1ValidateTokenRequest)
        return v1_validate_token_request_to_jsonable(obj, path=path)

    if exp == V1ValidateTokenResponse:
        assert isinstance(obj, V1ValidateTokenResponse)
        return v1_validate_token_response_to_jsonable(obj, path=path)

    raise ValueError("Unexpected `expected` type: {}".format(exp))


class Hubv1Tag:
    def __init__(self, key: Optional[str] = None, value: Optional[str] = None) -> None:
        """Initializes with the given values."""
        self.key = key

        self.value = value

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to hubv1_tag_to_jsonable.

        :return: JSON-able representation
        """
        return hubv1_tag_to_jsonable(self)


def new_hubv1_tag() -> Hubv1Tag:
    """Generates an instance of Hubv1Tag with default values."""
    return Hubv1Tag()


def hubv1_tag_from_obj(obj: Any, path: str = "") -> Hubv1Tag:
    """
    Generates an instance of Hubv1Tag from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of Hubv1Tag
    :param path: path to the object used for debugging
    :return: parsed instance of Hubv1Tag
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_key = obj.get("key", None)
    if obj_key is not None:
        key_from_obj = from_obj(
            obj_key, expected=[str], path=path + ".key"
        )  # type: Optional[str]
    else:
        key_from_obj = None

    obj_value = obj.get("value", None)
    if obj_value is not None:
        value_from_obj = from_obj(
            obj_value, expected=[str], path=path + ".value"
        )  # type: Optional[str]
    else:
        value_from_obj = None

    return Hubv1Tag(key=key_from_obj, value=value_from_obj)


def hubv1_tag_to_jsonable(
    hubv1_tag: Hubv1Tag, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of Hubv1Tag.

    :param hubv1_tag: instance of Hubv1Tag to be JSON-ized
    :param path: path to the hubv1_tag used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if hubv1_tag.key is not None:
        res["key"] = hubv1_tag.key

    if hubv1_tag.value is not None:
        res["value"] = hubv1_tag.value

    return res


class RpcStatus:
    def __init__(
        self,
        code: Optional[int] = None,
        message: Optional[str] = None,
        details: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.code = code

        self.message = message

        self.details = details

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to rpc_status_to_jsonable.

        :return: JSON-able representation
        """
        return rpc_status_to_jsonable(self)


def new_rpc_status() -> RpcStatus:
    """Generates an instance of RpcStatus with default values."""
    return RpcStatus()


def rpc_status_from_obj(obj: Any, path: str = "") -> RpcStatus:
    """
    Generates an instance of RpcStatus from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of RpcStatus
    :param path: path to the object used for debugging
    :return: parsed instance of RpcStatus
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_code = obj.get("code", None)
    if obj_code is not None:
        code_from_obj = from_obj(
            obj_code, expected=[int], path=path + ".code"
        )  # type: Optional[int]
    else:
        code_from_obj = None

    obj_message = obj.get("message", None)
    if obj_message is not None:
        message_from_obj = from_obj(
            obj_message, expected=[str], path=path + ".message"
        )  # type: Optional[str]
    else:
        message_from_obj = None

    obj_details = obj.get("details", None)
    if obj_details is not None:
        details_from_obj = from_obj(
            obj_details, expected=[list, dict, Any], path=path + ".details"
        )  # type: Optional[List[Dict[str, Any]]]
    else:
        details_from_obj = None

    return RpcStatus(
        code=code_from_obj, message=message_from_obj, details=details_from_obj
    )


def rpc_status_to_jsonable(
    rpc_status: RpcStatus, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of RpcStatus.

    :param rpc_status: instance of RpcStatus to be JSON-ized
    :param path: path to the rpc_status used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if rpc_status.code is not None:
        res["code"] = rpc_status.code

    if rpc_status.message is not None:
        res["message"] = rpc_status.message

    if rpc_status.details is not None:
        res["details"] = to_jsonable(
            rpc_status.details,
            expected=[list, dict, Any],
            path="{}.details".format(path),
        )

    return res


class V1BrowserConfig:
    """
    BrowserConfig describes the current configuration for one Feature.
    Instead of being simply enabled or disabled, features are enabled for a
    particular percentage of clients (0% is entirely disabled, 100% is entirely enabled).
    Clients are required to self-select a percentile value from 1 to 100 in a way that is random
    and trusted to consider a Feature disabled if it is disabled for the selected percentile.
    action_code_disabled describes what the Browser is expected to do if the Feature is not enabled for
    their assigned percentile.
    message_disabled may be displayed as a fallback action.
    action_code_enabled describes what the Browser is expected to do if the Feature is enabled for
    their assigned percentile. This enabled degraded modes. Can be empty.
    message_enabled may be displayed while in degraded mode. Can be empty.
    Likely additional fields will be added here as the Browser SDK behavior set becomes more complex.
    """

    def __init__(
        self,
        enabled_percent: Optional[int] = None,
        action_code_enabled: Optional[int] = None,
        message_enabled: Optional[str] = None,
        action_code_disabled: Optional[int] = None,
        message_disabled: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        self.enabled_percent = enabled_percent

        self.action_code_enabled = action_code_enabled

        self.message_enabled = message_enabled

        self.action_code_disabled = action_code_disabled

        self.message_disabled = message_disabled

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_browser_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_browser_config_to_jsonable(self)


def new_v1_browser_config() -> V1BrowserConfig:
    """Generates an instance of V1BrowserConfig with default values."""
    return V1BrowserConfig()


def v1_browser_config_from_obj(obj: Any, path: str = "") -> V1BrowserConfig:
    """
    Generates an instance of V1BrowserConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1BrowserConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1BrowserConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_enabled_percent = obj.get("enabledPercent", None)
    if obj_enabled_percent is not None:
        enabled_percent_from_obj = from_obj(
            obj_enabled_percent, expected=[int], path=path + ".enabledPercent"
        )  # type: Optional[int]
    else:
        enabled_percent_from_obj = None

    obj_action_code_enabled = obj.get("actionCodeEnabled", None)
    if obj_action_code_enabled is not None:
        action_code_enabled_from_obj = from_obj(
            obj_action_code_enabled, expected=[int], path=path + ".actionCodeEnabled"
        )  # type: Optional[int]
    else:
        action_code_enabled_from_obj = None

    obj_message_enabled = obj.get("messageEnabled", None)
    if obj_message_enabled is not None:
        message_enabled_from_obj = from_obj(
            obj_message_enabled, expected=[str], path=path + ".messageEnabled"
        )  # type: Optional[str]
    else:
        message_enabled_from_obj = None

    obj_action_code_disabled = obj.get("actionCodeDisabled", None)
    if obj_action_code_disabled is not None:
        action_code_disabled_from_obj = from_obj(
            obj_action_code_disabled, expected=[int], path=path + ".actionCodeDisabled"
        )  # type: Optional[int]
    else:
        action_code_disabled_from_obj = None

    obj_message_disabled = obj.get("messageDisabled", None)
    if obj_message_disabled is not None:
        message_disabled_from_obj = from_obj(
            obj_message_disabled, expected=[str], path=path + ".messageDisabled"
        )  # type: Optional[str]
    else:
        message_disabled_from_obj = None

    return V1BrowserConfig(
        enabled_percent=enabled_percent_from_obj,
        action_code_enabled=action_code_enabled_from_obj,
        message_enabled=message_enabled_from_obj,
        action_code_disabled=action_code_disabled_from_obj,
        message_disabled=message_disabled_from_obj,
    )


def v1_browser_config_to_jsonable(
    v1_browser_config: V1BrowserConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1BrowserConfig.

    :param v1_browser_config: instance of V1BrowserConfig to be JSON-ized
    :param path: path to the v1_browser_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_browser_config.enabled_percent is not None:
        res["enabledPercent"] = v1_browser_config.enabled_percent

    if v1_browser_config.action_code_enabled is not None:
        res["actionCodeEnabled"] = v1_browser_config.action_code_enabled

    if v1_browser_config.message_enabled is not None:
        res["messageEnabled"] = v1_browser_config.message_enabled

    if v1_browser_config.action_code_disabled is not None:
        res["actionCodeDisabled"] = v1_browser_config.action_code_disabled

    if v1_browser_config.message_disabled is not None:
        res["messageDisabled"] = v1_browser_config.message_disabled

    return res


class V1FeatureConfig:
    def __init__(
        self, name: Optional[str] = None, config: Optional["V1BrowserConfig"] = None
    ) -> None:
        """Initializes with the given values."""
        self.name = name

        self.config = config

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_feature_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_feature_config_to_jsonable(self)


def new_v1_feature_config() -> V1FeatureConfig:
    """Generates an instance of V1FeatureConfig with default values."""
    return V1FeatureConfig()


def v1_feature_config_from_obj(obj: Any, path: str = "") -> V1FeatureConfig:
    """
    Generates an instance of V1FeatureConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1FeatureConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1FeatureConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_name = obj.get("name", None)
    if obj_name is not None:
        name_from_obj = from_obj(
            obj_name, expected=[str], path=path + ".name"
        )  # type: Optional[str]
    else:
        name_from_obj = None

    obj_config = obj.get("config", None)
    if obj_config is not None:
        config_from_obj = from_obj(
            obj_config, expected=[V1BrowserConfig], path=path + ".config"
        )  # type: Optional['V1BrowserConfig']
    else:
        config_from_obj = None

    return V1FeatureConfig(name=name_from_obj, config=config_from_obj)


def v1_feature_config_to_jsonable(
    v1_feature_config: V1FeatureConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1FeatureConfig.

    :param v1_feature_config: instance of V1FeatureConfig to be JSON-ized
    :param path: path to the v1_feature_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_feature_config.name is not None:
        res["name"] = v1_feature_config.name

    if v1_feature_config.config is not None:
        res["config"] = to_jsonable(
            v1_feature_config.config,
            expected=[V1BrowserConfig],
            path="{}.config".format(path),
        )

    return res


class V1FeatureSelector:
    def __init__(
        self,
        environment: str,
        names: Optional[List[str]] = None,
        tags: Optional[List["Hubv1Tag"]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.environment = environment

        self.names = names

        self.tags = tags

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_feature_selector_to_jsonable.

        :return: JSON-able representation
        """
        return v1_feature_selector_to_jsonable(self)


def new_v1_feature_selector() -> V1FeatureSelector:
    """Generates an instance of V1FeatureSelector with default values."""
    return V1FeatureSelector(environment="")


def v1_feature_selector_from_obj(obj: Any, path: str = "") -> V1FeatureSelector:
    """
    Generates an instance of V1FeatureSelector from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1FeatureSelector
    :param path: path to the object used for debugging
    :return: parsed instance of V1FeatureSelector
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    environment_from_obj = from_obj(
        obj["environment"], expected=[str], path=path + ".environment"
    )  # type: str

    obj_names = obj.get("names", None)
    if obj_names is not None:
        names_from_obj = from_obj(
            obj_names, expected=[list, str], path=path + ".names"
        )  # type: Optional[List[str]]
    else:
        names_from_obj = None

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    return V1FeatureSelector(
        environment=environment_from_obj, names=names_from_obj, tags=tags_from_obj
    )


def v1_feature_selector_to_jsonable(
    v1_feature_selector: V1FeatureSelector, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1FeatureSelector.

    :param v1_feature_selector: instance of V1FeatureSelector to be JSON-ized
    :param path: path to the v1_feature_selector used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["environment"] = v1_feature_selector.environment

    if v1_feature_selector.names is not None:
        res["names"] = to_jsonable(
            v1_feature_selector.names,
            expected=[list, str],
            path="{}.names".format(path),
        )

    if v1_feature_selector.tags is not None:
        res["tags"] = to_jsonable(
            v1_feature_selector.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    return res


class V1GetBearerTokenResponse:
    """GetBearerTokenResponse is a new Bearer Token."""

    def __init__(self, bearer_token: Optional[str] = None) -> None:
        """Initializes with the given values."""
        self.bearer_token = bearer_token

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_bearer_token_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_bearer_token_response_to_jsonable(self)


def new_v1_get_bearer_token_response() -> V1GetBearerTokenResponse:
    """Generates an instance of V1GetBearerTokenResponse with default values."""
    return V1GetBearerTokenResponse()


def v1_get_bearer_token_response_from_obj(
    obj: Any, path: str = ""
) -> V1GetBearerTokenResponse:
    """
    Generates an instance of V1GetBearerTokenResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetBearerTokenResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetBearerTokenResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_bearer_token = obj.get("bearerToken", None)
    if obj_bearer_token is not None:
        bearer_token_from_obj = from_obj(
            obj_bearer_token, expected=[str], path=path + ".bearerToken"
        )  # type: Optional[str]
    else:
        bearer_token_from_obj = None

    return V1GetBearerTokenResponse(bearer_token=bearer_token_from_obj)


def v1_get_bearer_token_response_to_jsonable(
    v1_get_bearer_token_response: V1GetBearerTokenResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetBearerTokenResponse.

    :param v1_get_bearer_token_response: instance of V1GetBearerTokenResponse to be JSON-ized
    :param path: path to the v1_get_bearer_token_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_bearer_token_response.bearer_token is not None:
        res["bearerToken"] = v1_get_bearer_token_response.bearer_token

    return res


class V1GetBrowserContextRequest:
    """The request from Browser SDKs for a Browser Context. SDKs are expected to periodically poll, giving the version of the most recent configuration seen. Configurations may be large; we will not re-send them unless they have changed."""

    def __init__(self, feature: Optional["V1FeatureSelector"] = None) -> None:
        """Initializes with the given values."""
        # Information required to select and return the most recent BrowserContext version. If Feature names is nil, will return all Features in the organization associated with the bearer token/API key, otherwise only information related to the named Features will be returned.
        self.feature = feature

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_browser_context_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_browser_context_request_to_jsonable(self)


def new_v1_get_browser_context_request() -> V1GetBrowserContextRequest:
    """Generates an instance of V1GetBrowserContextRequest with default values."""
    return V1GetBrowserContextRequest()


def v1_get_browser_context_request_from_obj(
    obj: Any, path: str = ""
) -> V1GetBrowserContextRequest:
    """
    Generates an instance of V1GetBrowserContextRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetBrowserContextRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetBrowserContextRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_feature = obj.get("feature", None)
    if obj_feature is not None:
        feature_from_obj = from_obj(
            obj_feature, expected=[V1FeatureSelector], path=path + ".feature"
        )  # type: Optional['V1FeatureSelector']
    else:
        feature_from_obj = None

    return V1GetBrowserContextRequest(feature=feature_from_obj)


def v1_get_browser_context_request_to_jsonable(
    v1_get_browser_context_request: V1GetBrowserContextRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetBrowserContextRequest.

    :param v1_get_browser_context_request: instance of V1GetBrowserContextRequest to be JSON-ized
    :param path: path to the v1_get_browser_context_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_browser_context_request.feature is not None:
        res["feature"] = to_jsonable(
            v1_get_browser_context_request.feature,
            expected=[V1FeatureSelector],
            path="{}.feature".format(path),
        )

    return res


class V1GetBrowserContextResponse:
    """The response to Browser SDKs is designed to be cacheable for short periods. It is also designed to be shareable between multiple clients (e.g. in case of SSR or use of CDN etc). May return 304 Not Modified with ETag header and empty payload."""

    def __init__(
        self, feature_configs: Optional[List["V1FeatureConfig"]] = None
    ) -> None:
        """Initializes with the given values."""
        self.feature_configs = feature_configs

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_browser_context_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_browser_context_response_to_jsonable(self)


def new_v1_get_browser_context_response() -> V1GetBrowserContextResponse:
    """Generates an instance of V1GetBrowserContextResponse with default values."""
    return V1GetBrowserContextResponse()


def v1_get_browser_context_response_from_obj(
    obj: Any, path: str = ""
) -> V1GetBrowserContextResponse:
    """
    Generates an instance of V1GetBrowserContextResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetBrowserContextResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetBrowserContextResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_feature_configs = obj.get("featureConfigs", None)
    if obj_feature_configs is not None:
        feature_configs_from_obj = from_obj(
            obj_feature_configs,
            expected=[list, V1FeatureConfig],
            path=path + ".featureConfigs",
        )  # type: Optional[List['V1FeatureConfig']]
    else:
        feature_configs_from_obj = None

    return V1GetBrowserContextResponse(feature_configs=feature_configs_from_obj)


def v1_get_browser_context_response_to_jsonable(
    v1_get_browser_context_response: V1GetBrowserContextResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetBrowserContextResponse.

    :param v1_get_browser_context_response: instance of V1GetBrowserContextResponse to be JSON-ized
    :param path: path to the v1_get_browser_context_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_browser_context_response.feature_configs is not None:
        res["featureConfigs"] = to_jsonable(
            v1_get_browser_context_response.feature_configs,
            expected=[list, V1FeatureConfig],
            path="{}.featureConfigs".format(path),
        )

    return res


class V1GetGuardConfigRequest:
    """Request from Backend SDKs for a Guard Config. SDKs are expected to periodically poll, giving the version of the most recent configuration seen. Configurations may be large; we will not re-send them unless they have changed. Guard configurations may vary between environments but are SHARED between Services."""

    def __init__(
        self,
        version_seen: Optional[str] = None,
        selector: Optional["V1GuardServiceSelector"] = None,
    ) -> None:
        """Initializes with the given values."""
        # Set if the client has seen a previous version of the config. Server will send data only if newer config available.
        self.version_seen = version_seen

        # Information required to select and return the correct GuardConfig version.
        self.selector = selector

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_guard_config_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_guard_config_request_to_jsonable(self)


def new_v1_get_guard_config_request() -> V1GetGuardConfigRequest:
    """Generates an instance of V1GetGuardConfigRequest with default values."""
    return V1GetGuardConfigRequest()


def v1_get_guard_config_request_from_obj(
    obj: Any, path: str = ""
) -> V1GetGuardConfigRequest:
    """
    Generates an instance of V1GetGuardConfigRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetGuardConfigRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetGuardConfigRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_version_seen = obj.get("versionSeen", None)
    if obj_version_seen is not None:
        version_seen_from_obj = from_obj(
            obj_version_seen, expected=[str], path=path + ".versionSeen"
        )  # type: Optional[str]
    else:
        version_seen_from_obj = None

    obj_selector = obj.get("selector", None)
    if obj_selector is not None:
        selector_from_obj = from_obj(
            obj_selector, expected=[V1GuardServiceSelector], path=path + ".selector"
        )  # type: Optional['V1GuardServiceSelector']
    else:
        selector_from_obj = None

    return V1GetGuardConfigRequest(
        version_seen=version_seen_from_obj, selector=selector_from_obj
    )


def v1_get_guard_config_request_to_jsonable(
    v1_get_guard_config_request: V1GetGuardConfigRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetGuardConfigRequest.

    :param v1_get_guard_config_request: instance of V1GetGuardConfigRequest to be JSON-ized
    :param path: path to the v1_get_guard_config_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_guard_config_request.version_seen is not None:
        res["versionSeen"] = v1_get_guard_config_request.version_seen

    if v1_get_guard_config_request.selector is not None:
        res["selector"] = to_jsonable(
            v1_get_guard_config_request.selector,
            expected=[V1GuardServiceSelector],
            path="{}.selector".format(path),
        )

    return res


class V1GetGuardConfigResponse:
    """The response from Hub to Backend SDKs. Note that `config_data_sent` will be false and `config` will be empty if we did not have a newer config version than `version_seen`."""

    def __init__(
        self,
        version: Optional[str] = None,
        config_data_sent: Optional[bool] = None,
        config: Optional["V1GuardConfig"] = None,
    ) -> None:
        """Initializes with the given values."""
        self.version = version

        self.config_data_sent = config_data_sent

        self.config = config

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_guard_config_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_guard_config_response_to_jsonable(self)


def new_v1_get_guard_config_response() -> V1GetGuardConfigResponse:
    """Generates an instance of V1GetGuardConfigResponse with default values."""
    return V1GetGuardConfigResponse()


def v1_get_guard_config_response_from_obj(
    obj: Any, path: str = ""
) -> V1GetGuardConfigResponse:
    """
    Generates an instance of V1GetGuardConfigResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetGuardConfigResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetGuardConfigResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_version = obj.get("version", None)
    if obj_version is not None:
        version_from_obj = from_obj(
            obj_version, expected=[str], path=path + ".version"
        )  # type: Optional[str]
    else:
        version_from_obj = None

    obj_config_data_sent = obj.get("configDataSent", None)
    if obj_config_data_sent is not None:
        config_data_sent_from_obj = from_obj(
            obj_config_data_sent, expected=[bool], path=path + ".configDataSent"
        )  # type: Optional[bool]
    else:
        config_data_sent_from_obj = None

    obj_config = obj.get("config", None)
    if obj_config is not None:
        config_from_obj = from_obj(
            obj_config, expected=[V1GuardConfig], path=path + ".config"
        )  # type: Optional['V1GuardConfig']
    else:
        config_from_obj = None

    return V1GetGuardConfigResponse(
        version=version_from_obj,
        config_data_sent=config_data_sent_from_obj,
        config=config_from_obj,
    )


def v1_get_guard_config_response_to_jsonable(
    v1_get_guard_config_response: V1GetGuardConfigResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetGuardConfigResponse.

    :param v1_get_guard_config_response: instance of V1GetGuardConfigResponse to be JSON-ized
    :param path: path to the v1_get_guard_config_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_guard_config_response.version is not None:
        res["version"] = v1_get_guard_config_response.version

    if v1_get_guard_config_response.config_data_sent is not None:
        res["configDataSent"] = v1_get_guard_config_response.config_data_sent

    if v1_get_guard_config_response.config is not None:
        res["config"] = to_jsonable(
            v1_get_guard_config_response.config,
            expected=[V1GuardConfig],
            path="{}.config".format(path),
        )

    return res


class V1GetServiceConfigRequest:
    """The request from Backend SDKs for a Service Config. SDKs are expected to periodically poll, giving the version of the most recent configuration seen. Configurations may be large; we will not re-send them unless they have changed."""

    def __init__(
        self,
        version_seen: Optional[str] = None,
        service: Optional["V1ServiceSelector"] = None,
        client_id: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        # Set if the client has seen a previous version of the config. Server will send data only if newer config available.
        self.version_seen = version_seen

        self.service = service

        # This is the same stable client_id that is used when requesting quota via GetTokenRequest/GetTokenLeaseRequest endpoints.
        # If supplied, it permits Stanza to provide per-service telemetry and report on service<>guard and service<>feature relationships.
        self.client_id = client_id

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_service_config_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_service_config_request_to_jsonable(self)


def new_v1_get_service_config_request() -> V1GetServiceConfigRequest:
    """Generates an instance of V1GetServiceConfigRequest with default values."""
    return V1GetServiceConfigRequest()


def v1_get_service_config_request_from_obj(
    obj: Any, path: str = ""
) -> V1GetServiceConfigRequest:
    """
    Generates an instance of V1GetServiceConfigRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetServiceConfigRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetServiceConfigRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_version_seen = obj.get("versionSeen", None)
    if obj_version_seen is not None:
        version_seen_from_obj = from_obj(
            obj_version_seen, expected=[str], path=path + ".versionSeen"
        )  # type: Optional[str]
    else:
        version_seen_from_obj = None

    obj_service = obj.get("service", None)
    if obj_service is not None:
        service_from_obj = from_obj(
            obj_service, expected=[V1ServiceSelector], path=path + ".service"
        )  # type: Optional['V1ServiceSelector']
    else:
        service_from_obj = None

    obj_client_id = obj.get("clientId", None)
    if obj_client_id is not None:
        client_id_from_obj = from_obj(
            obj_client_id, expected=[str], path=path + ".clientId"
        )  # type: Optional[str]
    else:
        client_id_from_obj = None

    return V1GetServiceConfigRequest(
        version_seen=version_seen_from_obj,
        service=service_from_obj,
        client_id=client_id_from_obj,
    )


def v1_get_service_config_request_to_jsonable(
    v1_get_service_config_request: V1GetServiceConfigRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetServiceConfigRequest.

    :param v1_get_service_config_request: instance of V1GetServiceConfigRequest to be JSON-ized
    :param path: path to the v1_get_service_config_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_service_config_request.version_seen is not None:
        res["versionSeen"] = v1_get_service_config_request.version_seen

    if v1_get_service_config_request.service is not None:
        res["service"] = to_jsonable(
            v1_get_service_config_request.service,
            expected=[V1ServiceSelector],
            path="{}.service".format(path),
        )

    if v1_get_service_config_request.client_id is not None:
        res["clientId"] = v1_get_service_config_request.client_id

    return res


class V1GetServiceConfigResponse:
    """The response to Backend SDKs. Note that `config_data_sent` will be false and `config` will be empty if we did not have a newer config version than `version_seen`."""

    def __init__(
        self,
        version: Optional[str] = None,
        config_data_sent: Optional[bool] = None,
        config: Optional["V1ServiceConfig"] = None,
    ) -> None:
        """Initializes with the given values."""
        self.version = version

        self.config_data_sent = config_data_sent

        self.config = config

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_service_config_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_service_config_response_to_jsonable(self)


def new_v1_get_service_config_response() -> V1GetServiceConfigResponse:
    """Generates an instance of V1GetServiceConfigResponse with default values."""
    return V1GetServiceConfigResponse()


def v1_get_service_config_response_from_obj(
    obj: Any, path: str = ""
) -> V1GetServiceConfigResponse:
    """
    Generates an instance of V1GetServiceConfigResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetServiceConfigResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetServiceConfigResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_version = obj.get("version", None)
    if obj_version is not None:
        version_from_obj = from_obj(
            obj_version, expected=[str], path=path + ".version"
        )  # type: Optional[str]
    else:
        version_from_obj = None

    obj_config_data_sent = obj.get("configDataSent", None)
    if obj_config_data_sent is not None:
        config_data_sent_from_obj = from_obj(
            obj_config_data_sent, expected=[bool], path=path + ".configDataSent"
        )  # type: Optional[bool]
    else:
        config_data_sent_from_obj = None

    obj_config = obj.get("config", None)
    if obj_config is not None:
        config_from_obj = from_obj(
            obj_config, expected=[V1ServiceConfig], path=path + ".config"
        )  # type: Optional['V1ServiceConfig']
    else:
        config_from_obj = None

    return V1GetServiceConfigResponse(
        version=version_from_obj,
        config_data_sent=config_data_sent_from_obj,
        config=config_from_obj,
    )


def v1_get_service_config_response_to_jsonable(
    v1_get_service_config_response: V1GetServiceConfigResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetServiceConfigResponse.

    :param v1_get_service_config_response: instance of V1GetServiceConfigResponse to be JSON-ized
    :param path: path to the v1_get_service_config_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_service_config_response.version is not None:
        res["version"] = v1_get_service_config_response.version

    if v1_get_service_config_response.config_data_sent is not None:
        res["configDataSent"] = v1_get_service_config_response.config_data_sent

    if v1_get_service_config_response.config is not None:
        res["config"] = to_jsonable(
            v1_get_service_config_response.config,
            expected=[V1ServiceConfig],
            path="{}.config".format(path),
        )

    return res


class V1GetTokenLeaseRequest:
    """Requests token lease for given Guard at priority of specified feature."""

    def __init__(
        self,
        selector: "V1GuardFeatureSelector",
        client_id: Optional[str] = None,
        priority_boost: Optional[int] = None,
        default_weight: Optional[float] = None,
    ) -> None:
        """Initializes with the given values."""
        # Only tags which are used for quota management should be included here - i.e. the list of quota_tags returned by the GetGuardConfig endpoint for this Guard. If tags are in use only one quota token will be issued at a time.
        self.selector = selector

        # Used for tracking per-client token usage, allowing automatic determination of efficient batch leases. ID should be assigned by Stanza clients and be unique per-customer. Host or instance names may be used, or a UUID.
        # It is important that this value be stable over the lifetime of an instance: if it changes, then Stanza will not be able to efficiently assign batches of tokens.
        self.client_id = client_id

        # Used to boost priority - SDK can increase or decrease priority of request, relative to normal feature priority. For instance, a customer may wish to boost the priority of paid user traffic over free tier. Priority boosts may also be negative - for example, one might deprioritise bot traffic.
        self.priority_boost = priority_boost

        # Used for request weighting, i.e. accounting for varying request sizes and costs. The value set here is the default request weight which should be assumed for leases. If not specified, then the median weight is used when granted leases. Actual weights should be set via the SetTokenLeaseConsumed rpc.
        #
        # default_weight is optional; if not used then it is assumed that all requests have weight of 1.
        self.default_weight = default_weight

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_token_lease_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_token_lease_request_to_jsonable(self)


def new_v1_get_token_lease_request() -> V1GetTokenLeaseRequest:
    """Generates an instance of V1GetTokenLeaseRequest with default values."""
    return V1GetTokenLeaseRequest(selector=new_v1_guard_feature_selector())


def v1_get_token_lease_request_from_obj(
    obj: Any, path: str = ""
) -> V1GetTokenLeaseRequest:
    """
    Generates an instance of V1GetTokenLeaseRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetTokenLeaseRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetTokenLeaseRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    selector_from_obj = from_obj(
        obj["selector"], expected=[V1GuardFeatureSelector], path=path + ".selector"
    )  # type: 'V1GuardFeatureSelector'

    obj_client_id = obj.get("clientId", None)
    if obj_client_id is not None:
        client_id_from_obj = from_obj(
            obj_client_id, expected=[str], path=path + ".clientId"
        )  # type: Optional[str]
    else:
        client_id_from_obj = None

    obj_priority_boost = obj.get("priorityBoost", None)
    if obj_priority_boost is not None:
        priority_boost_from_obj = from_obj(
            obj_priority_boost, expected=[int], path=path + ".priorityBoost"
        )  # type: Optional[int]
    else:
        priority_boost_from_obj = None

    obj_default_weight = obj.get("defaultWeight", None)
    if obj_default_weight is not None:
        default_weight_from_obj = from_obj(
            obj_default_weight, expected=[float], path=path + ".defaultWeight"
        )  # type: Optional[float]
    else:
        default_weight_from_obj = None

    return V1GetTokenLeaseRequest(
        selector=selector_from_obj,
        client_id=client_id_from_obj,
        priority_boost=priority_boost_from_obj,
        default_weight=default_weight_from_obj,
    )


def v1_get_token_lease_request_to_jsonable(
    v1_get_token_lease_request: V1GetTokenLeaseRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetTokenLeaseRequest.

    :param v1_get_token_lease_request: instance of V1GetTokenLeaseRequest to be JSON-ized
    :param path: path to the v1_get_token_lease_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["selector"] = to_jsonable(
        v1_get_token_lease_request.selector,
        expected=[V1GuardFeatureSelector],
        path="{}.selector".format(path),
    )

    if v1_get_token_lease_request.client_id is not None:
        res["clientId"] = v1_get_token_lease_request.client_id

    if v1_get_token_lease_request.priority_boost is not None:
        res["priorityBoost"] = v1_get_token_lease_request.priority_boost

    if v1_get_token_lease_request.default_weight is not None:
        res["defaultWeight"] = v1_get_token_lease_request.default_weight

    return res


class V1GetTokenLeaseResponse:
    def __init__(
        self, granted: bool, leases: Optional[List["V1TokenLease"]] = None
    ) -> None:
        """Initializes with the given values."""
        self.granted = granted

        self.leases = leases

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_token_lease_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_token_lease_response_to_jsonable(self)


def new_v1_get_token_lease_response() -> V1GetTokenLeaseResponse:
    """Generates an instance of V1GetTokenLeaseResponse with default values."""
    return V1GetTokenLeaseResponse(granted=False)


def v1_get_token_lease_response_from_obj(
    obj: Any, path: str = ""
) -> V1GetTokenLeaseResponse:
    """
    Generates an instance of V1GetTokenLeaseResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetTokenLeaseResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetTokenLeaseResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    granted_from_obj = from_obj(
        obj["granted"], expected=[bool], path=path + ".granted"
    )  # type: bool

    obj_leases = obj.get("leases", None)
    if obj_leases is not None:
        leases_from_obj = from_obj(
            obj_leases, expected=[list, V1TokenLease], path=path + ".leases"
        )  # type: Optional[List['V1TokenLease']]
    else:
        leases_from_obj = None

    return V1GetTokenLeaseResponse(granted=granted_from_obj, leases=leases_from_obj)


def v1_get_token_lease_response_to_jsonable(
    v1_get_token_lease_response: V1GetTokenLeaseResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetTokenLeaseResponse.

    :param v1_get_token_lease_response: instance of V1GetTokenLeaseResponse to be JSON-ized
    :param path: path to the v1_get_token_lease_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["granted"] = v1_get_token_lease_response.granted

    if v1_get_token_lease_response.leases is not None:
        res["leases"] = to_jsonable(
            v1_get_token_lease_response.leases,
            expected=[list, V1TokenLease],
            path="{}.leases".format(path),
        )

    return res


class V1GetTokenRequest:
    """Requests token for given Guard at priority of specified feature."""

    def __init__(
        self,
        selector: "V1GuardFeatureSelector",
        client_id: Optional[str] = None,
        priority_boost: Optional[int] = None,
        weight: Optional[float] = None,
    ) -> None:
        """Initializes with the given values."""
        # Only tags which are used for quota management should be included here - i.e. the list of quota_tags returned by the GetGuardConfig endpoint for this Guard. If tags are in use only one quota token will be issued at a time.
        self.selector = selector

        # Used for tracking per-client token usage, allowing automatic determination of efficient batch leases. ID should be assigned by Stanza clients and be unique per-customer. Host or instance names may be used, or a UUID.
        # It is important that this value be stable over the lifetime of an instance: if it changes, then Stanza will not be able to efficiently assign batches of tokens.
        self.client_id = client_id

        # Used to increase or decrease priority of request, relative to normal feature priority.
        self.priority_boost = priority_boost

        # Used for request weighting, i.e. accounting for varying request sizes and costs. If not specified then a default value of 1 is used. In cases where weights/costs are not known upfront, users can send an initial estimate as the weight, and then later, when the exact cost is known, send an updated weight via the SetTokenLeaseConsumed rpc.
        #
        # weight is optional; if not used then it is assumed that all requests have weight of 1.
        self.weight = weight

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_token_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_token_request_to_jsonable(self)


def new_v1_get_token_request() -> V1GetTokenRequest:
    """Generates an instance of V1GetTokenRequest with default values."""
    return V1GetTokenRequest(selector=new_v1_guard_feature_selector())


def v1_get_token_request_from_obj(obj: Any, path: str = "") -> V1GetTokenRequest:
    """
    Generates an instance of V1GetTokenRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetTokenRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetTokenRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    selector_from_obj = from_obj(
        obj["selector"], expected=[V1GuardFeatureSelector], path=path + ".selector"
    )  # type: 'V1GuardFeatureSelector'

    obj_client_id = obj.get("clientId", None)
    if obj_client_id is not None:
        client_id_from_obj = from_obj(
            obj_client_id, expected=[str], path=path + ".clientId"
        )  # type: Optional[str]
    else:
        client_id_from_obj = None

    obj_priority_boost = obj.get("priorityBoost", None)
    if obj_priority_boost is not None:
        priority_boost_from_obj = from_obj(
            obj_priority_boost, expected=[int], path=path + ".priorityBoost"
        )  # type: Optional[int]
    else:
        priority_boost_from_obj = None

    obj_weight = obj.get("weight", None)
    if obj_weight is not None:
        weight_from_obj = from_obj(
            obj_weight, expected=[float], path=path + ".weight"
        )  # type: Optional[float]
    else:
        weight_from_obj = None

    return V1GetTokenRequest(
        selector=selector_from_obj,
        client_id=client_id_from_obj,
        priority_boost=priority_boost_from_obj,
        weight=weight_from_obj,
    )


def v1_get_token_request_to_jsonable(
    v1_get_token_request: V1GetTokenRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetTokenRequest.

    :param v1_get_token_request: instance of V1GetTokenRequest to be JSON-ized
    :param path: path to the v1_get_token_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["selector"] = to_jsonable(
        v1_get_token_request.selector,
        expected=[V1GuardFeatureSelector],
        path="{}.selector".format(path),
    )

    if v1_get_token_request.client_id is not None:
        res["clientId"] = v1_get_token_request.client_id

    if v1_get_token_request.priority_boost is not None:
        res["priorityBoost"] = v1_get_token_request.priority_boost

    if v1_get_token_request.weight is not None:
        res["weight"] = v1_get_token_request.weight

    return res


class V1GetTokenResponse:
    """Specifies whether token granted."""

    def __init__(
        self,
        granted: bool,
        token: Optional[str] = None,
        reason: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        self.granted = granted

        self.token = token

        self.reason = reason

        self.mode = mode

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_token_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_token_response_to_jsonable(self)


def new_v1_get_token_response() -> V1GetTokenResponse:
    """Generates an instance of V1GetTokenResponse with default values."""
    return V1GetTokenResponse(granted=False)


def v1_get_token_response_from_obj(obj: Any, path: str = "") -> V1GetTokenResponse:
    """
    Generates an instance of V1GetTokenResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetTokenResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetTokenResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    granted_from_obj = from_obj(
        obj["granted"], expected=[bool], path=path + ".granted"
    )  # type: bool

    obj_token = obj.get("token", None)
    if obj_token is not None:
        token_from_obj = from_obj(
            obj_token, expected=[str], path=path + ".token"
        )  # type: Optional[str]
    else:
        token_from_obj = None

    obj_reason = obj.get("reason", None)
    if obj_reason is not None:
        reason_from_obj = from_obj(
            obj_reason, expected=[str], path=path + ".reason"
        )  # type: Optional[str]
    else:
        reason_from_obj = None

    obj_mode = obj.get("mode", None)
    if obj_mode is not None:
        mode_from_obj = from_obj(
            obj_mode, expected=[str], path=path + ".mode"
        )  # type: Optional[str]
    else:
        mode_from_obj = None

    return V1GetTokenResponse(
        granted=granted_from_obj,
        token=token_from_obj,
        reason=reason_from_obj,
        mode=mode_from_obj,
    )


def v1_get_token_response_to_jsonable(
    v1_get_token_response: V1GetTokenResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetTokenResponse.

    :param v1_get_token_response: instance of V1GetTokenResponse to be JSON-ized
    :param path: path to the v1_get_token_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["granted"] = v1_get_token_response.granted

    if v1_get_token_response.token is not None:
        res["token"] = v1_get_token_response.token

    if v1_get_token_response.reason is not None:
        res["reason"] = v1_get_token_response.reason

    if v1_get_token_response.mode is not None:
        res["mode"] = v1_get_token_response.mode

    return res


class V1GetUsageRequest:
    """Usage query."""

    def __init__(
        self,
        environment: str,
        start_ts: str,
        end_ts: str,
        guard: Optional[str] = None,
        guard_query_mode: Optional[str] = None,
        apikey: Optional[str] = None,
        feature: Optional[str] = None,
        feature_query_mode: Optional[str] = None,
        service: Optional[str] = None,
        service_query_mode: Optional[str] = None,
        priority: Optional[int] = None,
        priority_query_mode: Optional[str] = None,
        report_tags: Optional[List[str]] = None,
        tags: Optional[List["Hubv1Tag"]] = None,
        report_all_tags: Optional[bool] = None,
        step: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        # If specified, only stats relating to the tags and features in selector will be returned.
        #  If only guard and environment are specified, then stats relating to all tags and features will be returned.
        self.environment = environment

        self.start_ts = start_ts

        self.end_ts = end_ts

        # Query for stats for this specific guard. If not specified then stats for all guards are returned.
        self.guard = guard

        self.guard_query_mode = guard_query_mode

        # Query for stats where this specific APIKey was used. If not specified then stats for all APIKeys are returned.
        self.apikey = apikey

        # Query for stats about a specific feature. If not specified then stats for all features are returned.
        self.feature = feature

        self.feature_query_mode = feature_query_mode

        # Query for stats about a specific service. If not specified then stats for all services are returned.
        # Note that Stanza can only track service statistics if client_id is used when requesting service configuration at startup, and sent with quota requests.
        self.service = service

        self.service_query_mode = service_query_mode

        # Query for stats about a specific priority level. If not specified then stats for all priorities are returned.
        self.priority = priority

        self.priority_query_mode = priority_query_mode

        # Tags matching listed tag keys will be reported (individual timeseries returned for each value).
        self.report_tags = report_tags

        # Only stats relating to the specified tags will be returned.
        self.tags = tags

        # Report all tag values for all tags as separate timeseries. Overrides tags and report_tags params.
        self.report_all_tags = report_all_tags

        # 1m to 1w - m is minutes; h hours; d days; w weeks (7d). Defaults to a step that results in <100 results. Minimum step 1m.
        self.step = step

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_usage_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_usage_request_to_jsonable(self)


def new_v1_get_usage_request() -> V1GetUsageRequest:
    """Generates an instance of V1GetUsageRequest with default values."""
    return V1GetUsageRequest(environment="", start_ts="", end_ts="")


def v1_get_usage_request_from_obj(obj: Any, path: str = "") -> V1GetUsageRequest:
    """
    Generates an instance of V1GetUsageRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetUsageRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetUsageRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    environment_from_obj = from_obj(
        obj["environment"], expected=[str], path=path + ".environment"
    )  # type: str

    start_ts_from_obj = from_obj(
        obj["startTs"], expected=[str], path=path + ".startTs"
    )  # type: str

    end_ts_from_obj = from_obj(
        obj["endTs"], expected=[str], path=path + ".endTs"
    )  # type: str

    obj_guard = obj.get("guard", None)
    if obj_guard is not None:
        guard_from_obj = from_obj(
            obj_guard, expected=[str], path=path + ".guard"
        )  # type: Optional[str]
    else:
        guard_from_obj = None

    obj_guard_query_mode = obj.get("guardQueryMode", None)
    if obj_guard_query_mode is not None:
        guard_query_mode_from_obj = from_obj(
            obj_guard_query_mode, expected=[str], path=path + ".guardQueryMode"
        )  # type: Optional[str]
    else:
        guard_query_mode_from_obj = None

    obj_apikey = obj.get("apikey", None)
    if obj_apikey is not None:
        apikey_from_obj = from_obj(
            obj_apikey, expected=[str], path=path + ".apikey"
        )  # type: Optional[str]
    else:
        apikey_from_obj = None

    obj_feature = obj.get("feature", None)
    if obj_feature is not None:
        feature_from_obj = from_obj(
            obj_feature, expected=[str], path=path + ".feature"
        )  # type: Optional[str]
    else:
        feature_from_obj = None

    obj_feature_query_mode = obj.get("featureQueryMode", None)
    if obj_feature_query_mode is not None:
        feature_query_mode_from_obj = from_obj(
            obj_feature_query_mode, expected=[str], path=path + ".featureQueryMode"
        )  # type: Optional[str]
    else:
        feature_query_mode_from_obj = None

    obj_service = obj.get("service", None)
    if obj_service is not None:
        service_from_obj = from_obj(
            obj_service, expected=[str], path=path + ".service"
        )  # type: Optional[str]
    else:
        service_from_obj = None

    obj_service_query_mode = obj.get("serviceQueryMode", None)
    if obj_service_query_mode is not None:
        service_query_mode_from_obj = from_obj(
            obj_service_query_mode, expected=[str], path=path + ".serviceQueryMode"
        )  # type: Optional[str]
    else:
        service_query_mode_from_obj = None

    obj_priority = obj.get("priority", None)
    if obj_priority is not None:
        priority_from_obj = from_obj(
            obj_priority, expected=[int], path=path + ".priority"
        )  # type: Optional[int]
    else:
        priority_from_obj = None

    obj_priority_query_mode = obj.get("priorityQueryMode", None)
    if obj_priority_query_mode is not None:
        priority_query_mode_from_obj = from_obj(
            obj_priority_query_mode, expected=[str], path=path + ".priorityQueryMode"
        )  # type: Optional[str]
    else:
        priority_query_mode_from_obj = None

    obj_report_tags = obj.get("reportTags", None)
    if obj_report_tags is not None:
        report_tags_from_obj = from_obj(
            obj_report_tags, expected=[list, str], path=path + ".reportTags"
        )  # type: Optional[List[str]]
    else:
        report_tags_from_obj = None

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    obj_report_all_tags = obj.get("reportAllTags", None)
    if obj_report_all_tags is not None:
        report_all_tags_from_obj = from_obj(
            obj_report_all_tags, expected=[bool], path=path + ".reportAllTags"
        )  # type: Optional[bool]
    else:
        report_all_tags_from_obj = None

    obj_step = obj.get("step", None)
    if obj_step is not None:
        step_from_obj = from_obj(
            obj_step, expected=[str], path=path + ".step"
        )  # type: Optional[str]
    else:
        step_from_obj = None

    return V1GetUsageRequest(
        environment=environment_from_obj,
        start_ts=start_ts_from_obj,
        end_ts=end_ts_from_obj,
        guard=guard_from_obj,
        guard_query_mode=guard_query_mode_from_obj,
        apikey=apikey_from_obj,
        feature=feature_from_obj,
        feature_query_mode=feature_query_mode_from_obj,
        service=service_from_obj,
        service_query_mode=service_query_mode_from_obj,
        priority=priority_from_obj,
        priority_query_mode=priority_query_mode_from_obj,
        report_tags=report_tags_from_obj,
        tags=tags_from_obj,
        report_all_tags=report_all_tags_from_obj,
        step=step_from_obj,
    )


def v1_get_usage_request_to_jsonable(
    v1_get_usage_request: V1GetUsageRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetUsageRequest.

    :param v1_get_usage_request: instance of V1GetUsageRequest to be JSON-ized
    :param path: path to the v1_get_usage_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["environment"] = v1_get_usage_request.environment

    res["startTs"] = v1_get_usage_request.start_ts

    res["endTs"] = v1_get_usage_request.end_ts

    if v1_get_usage_request.guard is not None:
        res["guard"] = v1_get_usage_request.guard

    if v1_get_usage_request.guard_query_mode is not None:
        res["guardQueryMode"] = v1_get_usage_request.guard_query_mode

    if v1_get_usage_request.apikey is not None:
        res["apikey"] = v1_get_usage_request.apikey

    if v1_get_usage_request.feature is not None:
        res["feature"] = v1_get_usage_request.feature

    if v1_get_usage_request.feature_query_mode is not None:
        res["featureQueryMode"] = v1_get_usage_request.feature_query_mode

    if v1_get_usage_request.service is not None:
        res["service"] = v1_get_usage_request.service

    if v1_get_usage_request.service_query_mode is not None:
        res["serviceQueryMode"] = v1_get_usage_request.service_query_mode

    if v1_get_usage_request.priority is not None:
        res["priority"] = v1_get_usage_request.priority

    if v1_get_usage_request.priority_query_mode is not None:
        res["priorityQueryMode"] = v1_get_usage_request.priority_query_mode

    if v1_get_usage_request.report_tags is not None:
        res["reportTags"] = to_jsonable(
            v1_get_usage_request.report_tags,
            expected=[list, str],
            path="{}.reportTags".format(path),
        )

    if v1_get_usage_request.tags is not None:
        res["tags"] = to_jsonable(
            v1_get_usage_request.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    if v1_get_usage_request.report_all_tags is not None:
        res["reportAllTags"] = v1_get_usage_request.report_all_tags

    if v1_get_usage_request.step is not None:
        res["step"] = v1_get_usage_request.step

    return res


class V1GetUsageResponse:
    def __init__(self, result: Optional[List["V1UsageTimeseries"]] = None) -> None:
        """Initializes with the given values."""
        self.result = result

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_get_usage_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_get_usage_response_to_jsonable(self)


def new_v1_get_usage_response() -> V1GetUsageResponse:
    """Generates an instance of V1GetUsageResponse with default values."""
    return V1GetUsageResponse()


def v1_get_usage_response_from_obj(obj: Any, path: str = "") -> V1GetUsageResponse:
    """
    Generates an instance of V1GetUsageResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GetUsageResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1GetUsageResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_result = obj.get("result", None)
    if obj_result is not None:
        result_from_obj = from_obj(
            obj_result, expected=[list, V1UsageTimeseries], path=path + ".result"
        )  # type: Optional[List['V1UsageTimeseries']]
    else:
        result_from_obj = None

    return V1GetUsageResponse(result=result_from_obj)


def v1_get_usage_response_to_jsonable(
    v1_get_usage_response: V1GetUsageResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GetUsageResponse.

    :param v1_get_usage_response: instance of V1GetUsageResponse to be JSON-ized
    :param path: path to the v1_get_usage_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_get_usage_response.result is not None:
        res["result"] = to_jsonable(
            v1_get_usage_response.result,
            expected=[list, V1UsageTimeseries],
            path="{}.result".format(path),
        )

    return res


class V1GuardConfig:
    """
    GuardConfig represents a configuration for a given Stanza SDK instrumented Guard, which may be used by multiple services!
    If check_quota is false, then no ratelimiting will be performed. All quota requests will succeed and the SDK may short-circuit quota requests, i.e. not call Hub for quota.
    At a later point, there will be additional per-Guard configuration, such as deadline overrides, adaptive circuitbreaking configs, etc.
    """

    def __init__(
        self,
        validate_ingress_tokens: Optional[bool] = None,
        check_quota: Optional[bool] = None,
        quota_tags: Optional[List[str]] = None,
        report_only: Optional[bool] = None,
    ) -> None:
        """Initializes with the given values."""
        # Boolean representing wether to validate contents of the X-Stanza-Token header.
        self.validate_ingress_tokens = validate_ingress_tokens

        # Boolean representing whether quota checks are enabled.
        self.check_quota = check_quota

        # The set of tags which are used for quota management. For example, a 'customer_id' tag might be used to implement per-customer quota limits. Only the tags listed here should be included in GetToken and GetTokenLease requests.
        self.quota_tags = quota_tags

        # If report_only is true then the SDK should perform all load management logic and emit statistics, but never actually throttle or deny requests for any reason.
        # However, the SDK should emit accurate metrics about what actions would normally be taken if Report Only mode were not enabled. The purpose of this is to allow
        # users to assess the impact of enabling a Guard without risking over-throttling traffic.
        # The label mode="report_only" should be set on all metrics sent to Stanza.
        self.report_only = report_only

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_guard_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_guard_config_to_jsonable(self)


def new_v1_guard_config() -> V1GuardConfig:
    """Generates an instance of V1GuardConfig with default values."""
    return V1GuardConfig()


def v1_guard_config_from_obj(obj: Any, path: str = "") -> V1GuardConfig:
    """
    Generates an instance of V1GuardConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GuardConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1GuardConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_validate_ingress_tokens = obj.get("validateIngressTokens", None)
    if obj_validate_ingress_tokens is not None:
        validate_ingress_tokens_from_obj = from_obj(
            obj_validate_ingress_tokens,
            expected=[bool],
            path=path + ".validateIngressTokens",
        )  # type: Optional[bool]
    else:
        validate_ingress_tokens_from_obj = None

    obj_check_quota = obj.get("checkQuota", None)
    if obj_check_quota is not None:
        check_quota_from_obj = from_obj(
            obj_check_quota, expected=[bool], path=path + ".checkQuota"
        )  # type: Optional[bool]
    else:
        check_quota_from_obj = None

    obj_quota_tags = obj.get("quotaTags", None)
    if obj_quota_tags is not None:
        quota_tags_from_obj = from_obj(
            obj_quota_tags, expected=[list, str], path=path + ".quotaTags"
        )  # type: Optional[List[str]]
    else:
        quota_tags_from_obj = None

    obj_report_only = obj.get("reportOnly", None)
    if obj_report_only is not None:
        report_only_from_obj = from_obj(
            obj_report_only, expected=[bool], path=path + ".reportOnly"
        )  # type: Optional[bool]
    else:
        report_only_from_obj = None

    return V1GuardConfig(
        validate_ingress_tokens=validate_ingress_tokens_from_obj,
        check_quota=check_quota_from_obj,
        quota_tags=quota_tags_from_obj,
        report_only=report_only_from_obj,
    )


def v1_guard_config_to_jsonable(
    v1_guard_config: V1GuardConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GuardConfig.

    :param v1_guard_config: instance of V1GuardConfig to be JSON-ized
    :param path: path to the v1_guard_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_guard_config.validate_ingress_tokens is not None:
        res["validateIngressTokens"] = v1_guard_config.validate_ingress_tokens

    if v1_guard_config.check_quota is not None:
        res["checkQuota"] = v1_guard_config.check_quota

    if v1_guard_config.quota_tags is not None:
        res["quotaTags"] = to_jsonable(
            v1_guard_config.quota_tags,
            expected=[list, str],
            path="{}.quotaTags".format(path),
        )

    if v1_guard_config.report_only is not None:
        res["reportOnly"] = v1_guard_config.report_only

    return res


class V1GuardFeatureSelector:
    def __init__(
        self,
        environment: str,
        guard_name: str,
        feature_name: Optional[str] = None,
        tags: Optional[List["Hubv1Tag"]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.environment = environment

        self.guard_name = guard_name

        self.feature_name = feature_name

        self.tags = tags

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_guard_feature_selector_to_jsonable.

        :return: JSON-able representation
        """
        return v1_guard_feature_selector_to_jsonable(self)


def new_v1_guard_feature_selector() -> V1GuardFeatureSelector:
    """Generates an instance of V1GuardFeatureSelector with default values."""
    return V1GuardFeatureSelector(environment="", guard_name="")


def v1_guard_feature_selector_from_obj(
    obj: Any, path: str = ""
) -> V1GuardFeatureSelector:
    """
    Generates an instance of V1GuardFeatureSelector from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GuardFeatureSelector
    :param path: path to the object used for debugging
    :return: parsed instance of V1GuardFeatureSelector
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    environment_from_obj = from_obj(
        obj["environment"], expected=[str], path=path + ".environment"
    )  # type: str

    guard_name_from_obj = from_obj(
        obj["guardName"], expected=[str], path=path + ".guardName"
    )  # type: str

    obj_feature_name = obj.get("featureName", None)
    if obj_feature_name is not None:
        feature_name_from_obj = from_obj(
            obj_feature_name, expected=[str], path=path + ".featureName"
        )  # type: Optional[str]
    else:
        feature_name_from_obj = None

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    return V1GuardFeatureSelector(
        environment=environment_from_obj,
        guard_name=guard_name_from_obj,
        feature_name=feature_name_from_obj,
        tags=tags_from_obj,
    )


def v1_guard_feature_selector_to_jsonable(
    v1_guard_feature_selector: V1GuardFeatureSelector, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GuardFeatureSelector.

    :param v1_guard_feature_selector: instance of V1GuardFeatureSelector to be JSON-ized
    :param path: path to the v1_guard_feature_selector used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["environment"] = v1_guard_feature_selector.environment

    res["guardName"] = v1_guard_feature_selector.guard_name

    if v1_guard_feature_selector.feature_name is not None:
        res["featureName"] = v1_guard_feature_selector.feature_name

    if v1_guard_feature_selector.tags is not None:
        res["tags"] = to_jsonable(
            v1_guard_feature_selector.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    return res


class V1GuardSelector:
    def __init__(
        self, environment: str, name: str, tags: Optional[List["Hubv1Tag"]] = None
    ) -> None:
        """Initializes with the given values."""
        self.environment = environment

        self.name = name

        self.tags = tags

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_guard_selector_to_jsonable.

        :return: JSON-able representation
        """
        return v1_guard_selector_to_jsonable(self)


def new_v1_guard_selector() -> V1GuardSelector:
    """Generates an instance of V1GuardSelector with default values."""
    return V1GuardSelector(environment="", name="")


def v1_guard_selector_from_obj(obj: Any, path: str = "") -> V1GuardSelector:
    """
    Generates an instance of V1GuardSelector from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GuardSelector
    :param path: path to the object used for debugging
    :return: parsed instance of V1GuardSelector
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    environment_from_obj = from_obj(
        obj["environment"], expected=[str], path=path + ".environment"
    )  # type: str

    name_from_obj = from_obj(
        obj["name"], expected=[str], path=path + ".name"
    )  # type: str

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    return V1GuardSelector(
        environment=environment_from_obj, name=name_from_obj, tags=tags_from_obj
    )


def v1_guard_selector_to_jsonable(
    v1_guard_selector: V1GuardSelector, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GuardSelector.

    :param v1_guard_selector: instance of V1GuardSelector to be JSON-ized
    :param path: path to the v1_guard_selector used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["environment"] = v1_guard_selector.environment

    res["name"] = v1_guard_selector.name

    if v1_guard_selector.tags is not None:
        res["tags"] = to_jsonable(
            v1_guard_selector.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    return res


class V1GuardServiceSelector:
    def __init__(
        self,
        environment: str,
        guard_name: str,
        service_name: str,
        service_release: str,
        tags: Optional[List["Hubv1Tag"]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.environment = environment

        self.guard_name = guard_name

        self.service_name = service_name

        self.service_release = service_release

        self.tags = tags

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_guard_service_selector_to_jsonable.

        :return: JSON-able representation
        """
        return v1_guard_service_selector_to_jsonable(self)


def new_v1_guard_service_selector() -> V1GuardServiceSelector:
    """Generates an instance of V1GuardServiceSelector with default values."""
    return V1GuardServiceSelector(
        environment="", guard_name="", service_name="", service_release=""
    )


def v1_guard_service_selector_from_obj(
    obj: Any, path: str = ""
) -> V1GuardServiceSelector:
    """
    Generates an instance of V1GuardServiceSelector from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1GuardServiceSelector
    :param path: path to the object used for debugging
    :return: parsed instance of V1GuardServiceSelector
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    environment_from_obj = from_obj(
        obj["environment"], expected=[str], path=path + ".environment"
    )  # type: str

    guard_name_from_obj = from_obj(
        obj["guardName"], expected=[str], path=path + ".guardName"
    )  # type: str

    service_name_from_obj = from_obj(
        obj["serviceName"], expected=[str], path=path + ".serviceName"
    )  # type: str

    service_release_from_obj = from_obj(
        obj["serviceRelease"], expected=[str], path=path + ".serviceRelease"
    )  # type: str

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    return V1GuardServiceSelector(
        environment=environment_from_obj,
        guard_name=guard_name_from_obj,
        service_name=service_name_from_obj,
        service_release=service_release_from_obj,
        tags=tags_from_obj,
    )


def v1_guard_service_selector_to_jsonable(
    v1_guard_service_selector: V1GuardServiceSelector, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1GuardServiceSelector.

    :param v1_guard_service_selector: instance of V1GuardServiceSelector to be JSON-ized
    :param path: path to the v1_guard_service_selector used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["environment"] = v1_guard_service_selector.environment

    res["guardName"] = v1_guard_service_selector.guard_name

    res["serviceName"] = v1_guard_service_selector.service_name

    res["serviceRelease"] = v1_guard_service_selector.service_release

    if v1_guard_service_selector.tags is not None:
        res["tags"] = to_jsonable(
            v1_guard_service_selector.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    return res


class V1HeaderTraceConfig:
    """Specifies which headers should be sampled - required by OTel spec."""

    def __init__(
        self,
        span_selectors: Optional[List["V1SpanSelector"]] = None,
        request_header_names: Optional[List[str]] = None,
        response_header_names: Optional[List[str]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.span_selectors = span_selectors

        self.request_header_names = request_header_names

        self.response_header_names = response_header_names

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_header_trace_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_header_trace_config_to_jsonable(self)


def new_v1_header_trace_config() -> V1HeaderTraceConfig:
    """Generates an instance of V1HeaderTraceConfig with default values."""
    return V1HeaderTraceConfig()


def v1_header_trace_config_from_obj(obj: Any, path: str = "") -> V1HeaderTraceConfig:
    """
    Generates an instance of V1HeaderTraceConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1HeaderTraceConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1HeaderTraceConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_span_selectors = obj.get("spanSelectors", None)
    if obj_span_selectors is not None:
        span_selectors_from_obj = from_obj(
            obj_span_selectors,
            expected=[list, V1SpanSelector],
            path=path + ".spanSelectors",
        )  # type: Optional[List['V1SpanSelector']]
    else:
        span_selectors_from_obj = None

    obj_request_header_names = obj.get("requestHeaderNames", None)
    if obj_request_header_names is not None:
        request_header_names_from_obj = from_obj(
            obj_request_header_names,
            expected=[list, str],
            path=path + ".requestHeaderNames",
        )  # type: Optional[List[str]]
    else:
        request_header_names_from_obj = None

    obj_response_header_names = obj.get("responseHeaderNames", None)
    if obj_response_header_names is not None:
        response_header_names_from_obj = from_obj(
            obj_response_header_names,
            expected=[list, str],
            path=path + ".responseHeaderNames",
        )  # type: Optional[List[str]]
    else:
        response_header_names_from_obj = None

    return V1HeaderTraceConfig(
        span_selectors=span_selectors_from_obj,
        request_header_names=request_header_names_from_obj,
        response_header_names=response_header_names_from_obj,
    )


def v1_header_trace_config_to_jsonable(
    v1_header_trace_config: V1HeaderTraceConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1HeaderTraceConfig.

    :param v1_header_trace_config: instance of V1HeaderTraceConfig to be JSON-ized
    :param path: path to the v1_header_trace_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_header_trace_config.span_selectors is not None:
        res["spanSelectors"] = to_jsonable(
            v1_header_trace_config.span_selectors,
            expected=[list, V1SpanSelector],
            path="{}.spanSelectors".format(path),
        )

    if v1_header_trace_config.request_header_names is not None:
        res["requestHeaderNames"] = to_jsonable(
            v1_header_trace_config.request_header_names,
            expected=[list, str],
            path="{}.requestHeaderNames".format(path),
        )

    if v1_header_trace_config.response_header_names is not None:
        res["responseHeaderNames"] = to_jsonable(
            v1_header_trace_config.response_header_names,
            expected=[list, str],
            path="{}.responseHeaderNames".format(path),
        )

    return res


class V1MetricConfig:
    def __init__(self, collector_url: Optional[str] = None) -> None:
        """Initializes with the given values."""
        # URL of OTEL metric collector. If URL begins with http or https it will be treated as an HTTP collector, otherwise it will be treated as a gRPC collector.
        self.collector_url = collector_url

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_metric_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_metric_config_to_jsonable(self)


def new_v1_metric_config() -> V1MetricConfig:
    """Generates an instance of V1MetricConfig with default values."""
    return V1MetricConfig()


def v1_metric_config_from_obj(obj: Any, path: str = "") -> V1MetricConfig:
    """
    Generates an instance of V1MetricConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1MetricConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1MetricConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_collector_url = obj.get("collectorUrl", None)
    if obj_collector_url is not None:
        collector_url_from_obj = from_obj(
            obj_collector_url, expected=[str], path=path + ".collectorUrl"
        )  # type: Optional[str]
    else:
        collector_url_from_obj = None

    return V1MetricConfig(collector_url=collector_url_from_obj)


def v1_metric_config_to_jsonable(
    v1_metric_config: V1MetricConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1MetricConfig.

    :param v1_metric_config: instance of V1MetricConfig to be JSON-ized
    :param path: path to the v1_metric_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_metric_config.collector_url is not None:
        res["collectorUrl"] = v1_metric_config.collector_url

    return res


class V1ParamTraceConfig:
    """Specifies which request parameters should be sampled."""

    def __init__(
        self,
        span_selectors: Optional[List["V1SpanSelector"]] = None,
        parameter_names: Optional[List[str]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.span_selectors = span_selectors

        self.parameter_names = parameter_names

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_param_trace_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_param_trace_config_to_jsonable(self)


def new_v1_param_trace_config() -> V1ParamTraceConfig:
    """Generates an instance of V1ParamTraceConfig with default values."""
    return V1ParamTraceConfig()


def v1_param_trace_config_from_obj(obj: Any, path: str = "") -> V1ParamTraceConfig:
    """
    Generates an instance of V1ParamTraceConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1ParamTraceConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1ParamTraceConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_span_selectors = obj.get("spanSelectors", None)
    if obj_span_selectors is not None:
        span_selectors_from_obj = from_obj(
            obj_span_selectors,
            expected=[list, V1SpanSelector],
            path=path + ".spanSelectors",
        )  # type: Optional[List['V1SpanSelector']]
    else:
        span_selectors_from_obj = None

    obj_parameter_names = obj.get("parameterNames", None)
    if obj_parameter_names is not None:
        parameter_names_from_obj = from_obj(
            obj_parameter_names, expected=[list, str], path=path + ".parameterNames"
        )  # type: Optional[List[str]]
    else:
        parameter_names_from_obj = None

    return V1ParamTraceConfig(
        span_selectors=span_selectors_from_obj, parameter_names=parameter_names_from_obj
    )


def v1_param_trace_config_to_jsonable(
    v1_param_trace_config: V1ParamTraceConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1ParamTraceConfig.

    :param v1_param_trace_config: instance of V1ParamTraceConfig to be JSON-ized
    :param path: path to the v1_param_trace_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_param_trace_config.span_selectors is not None:
        res["spanSelectors"] = to_jsonable(
            v1_param_trace_config.span_selectors,
            expected=[list, V1SpanSelector],
            path="{}.spanSelectors".format(path),
        )

    if v1_param_trace_config.parameter_names is not None:
        res["parameterNames"] = to_jsonable(
            v1_param_trace_config.parameter_names,
            expected=[list, str],
            path="{}.parameterNames".format(path),
        )

    return res


class V1QueryGuardHealthRequest:
    """Called by SDK to determine whether a Guard is overloaded at a given Feature's priority level. Used so that customer code can make good decisions about fail-fast or graceful degradation as high up the stack as possible. SDK may cache the result for up to 10 seconds."""

    def __init__(
        self,
        selector: Optional["V1GuardFeatureSelector"] = None,
        priority_boost: Optional[int] = None,
    ) -> None:
        """Initializes with the given values."""
        # Only tags which are used for quota management should be included here - i.e. the list of quota_tags returned by the GetGuardConfig endpoint for this Guard. If tags are in use only one quota token will be issued at a time.
        #
        # Required: GuardName, featureName, environment
        self.selector = selector

        # Used to boost priority - SDK can increase or decrease priority of request, relative to normal feature priority. For instance, a customer may wish to boost the priority of paid user traffic over free tier. Priority boosts may also be negative - for example, one might deprioritise bot traffic.
        self.priority_boost = priority_boost

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_query_guard_health_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_query_guard_health_request_to_jsonable(self)


def new_v1_query_guard_health_request() -> V1QueryGuardHealthRequest:
    """Generates an instance of V1QueryGuardHealthRequest with default values."""
    return V1QueryGuardHealthRequest()


def v1_query_guard_health_request_from_obj(
    obj: Any, path: str = ""
) -> V1QueryGuardHealthRequest:
    """
    Generates an instance of V1QueryGuardHealthRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1QueryGuardHealthRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1QueryGuardHealthRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_selector = obj.get("selector", None)
    if obj_selector is not None:
        selector_from_obj = from_obj(
            obj_selector, expected=[V1GuardFeatureSelector], path=path + ".selector"
        )  # type: Optional['V1GuardFeatureSelector']
    else:
        selector_from_obj = None

    obj_priority_boost = obj.get("priorityBoost", None)
    if obj_priority_boost is not None:
        priority_boost_from_obj = from_obj(
            obj_priority_boost, expected=[int], path=path + ".priorityBoost"
        )  # type: Optional[int]
    else:
        priority_boost_from_obj = None

    return V1QueryGuardHealthRequest(
        selector=selector_from_obj, priority_boost=priority_boost_from_obj
    )


def v1_query_guard_health_request_to_jsonable(
    v1_query_guard_health_request: V1QueryGuardHealthRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1QueryGuardHealthRequest.

    :param v1_query_guard_health_request: instance of V1QueryGuardHealthRequest to be JSON-ized
    :param path: path to the v1_query_guard_health_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_query_guard_health_request.selector is not None:
        res["selector"] = to_jsonable(
            v1_query_guard_health_request.selector,
            expected=[V1GuardFeatureSelector],
            path="{}.selector".format(path),
        )

    if v1_query_guard_health_request.priority_boost is not None:
        res["priorityBoost"] = v1_query_guard_health_request.priority_boost

    return res


class V1QueryGuardHealthResponse:
    def __init__(self, health: Optional[str] = None) -> None:
        """Initializes with the given values."""
        self.health = health

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_query_guard_health_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_query_guard_health_response_to_jsonable(self)


def new_v1_query_guard_health_response() -> V1QueryGuardHealthResponse:
    """Generates an instance of V1QueryGuardHealthResponse with default values."""
    return V1QueryGuardHealthResponse()


def v1_query_guard_health_response_from_obj(
    obj: Any, path: str = ""
) -> V1QueryGuardHealthResponse:
    """
    Generates an instance of V1QueryGuardHealthResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1QueryGuardHealthResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1QueryGuardHealthResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_health = obj.get("health", None)
    if obj_health is not None:
        health_from_obj = from_obj(
            obj_health, expected=[str], path=path + ".health"
        )  # type: Optional[str]
    else:
        health_from_obj = None

    return V1QueryGuardHealthResponse(health=health_from_obj)


def v1_query_guard_health_response_to_jsonable(
    v1_query_guard_health_response: V1QueryGuardHealthResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1QueryGuardHealthResponse.

    :param v1_query_guard_health_response: instance of V1QueryGuardHealthResponse to be JSON-ized
    :param path: path to the v1_query_guard_health_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_query_guard_health_response.health is not None:
        res["health"] = v1_query_guard_health_response.health

    return res


class V1SentinelConfig:
    """SentinelConfig represents Sentinel compliant JSON configuration for the given Sentinel types. These rules are "per service" (not per Guard) with Guard specific routing encoded in the given JSON blobs (as Sentinel "Resources")."""

    def __init__(
        self,
        circuitbreaker_rules_json: Optional[str] = None,
        flow_rules_json: Optional[str] = None,
        isolation_rules_json: Optional[str] = None,
        system_rules_json: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        self.circuitbreaker_rules_json = circuitbreaker_rules_json

        self.flow_rules_json = flow_rules_json

        self.isolation_rules_json = isolation_rules_json

        self.system_rules_json = system_rules_json

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_sentinel_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_sentinel_config_to_jsonable(self)


def new_v1_sentinel_config() -> V1SentinelConfig:
    """Generates an instance of V1SentinelConfig with default values."""
    return V1SentinelConfig()


def v1_sentinel_config_from_obj(obj: Any, path: str = "") -> V1SentinelConfig:
    """
    Generates an instance of V1SentinelConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1SentinelConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1SentinelConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_circuitbreaker_rules_json = obj.get("circuitbreakerRulesJson", None)
    if obj_circuitbreaker_rules_json is not None:
        circuitbreaker_rules_json_from_obj = from_obj(
            obj_circuitbreaker_rules_json,
            expected=[str],
            path=path + ".circuitbreakerRulesJson",
        )  # type: Optional[str]
    else:
        circuitbreaker_rules_json_from_obj = None

    obj_flow_rules_json = obj.get("flowRulesJson", None)
    if obj_flow_rules_json is not None:
        flow_rules_json_from_obj = from_obj(
            obj_flow_rules_json, expected=[str], path=path + ".flowRulesJson"
        )  # type: Optional[str]
    else:
        flow_rules_json_from_obj = None

    obj_isolation_rules_json = obj.get("isolationRulesJson", None)
    if obj_isolation_rules_json is not None:
        isolation_rules_json_from_obj = from_obj(
            obj_isolation_rules_json, expected=[str], path=path + ".isolationRulesJson"
        )  # type: Optional[str]
    else:
        isolation_rules_json_from_obj = None

    obj_system_rules_json = obj.get("systemRulesJson", None)
    if obj_system_rules_json is not None:
        system_rules_json_from_obj = from_obj(
            obj_system_rules_json, expected=[str], path=path + ".systemRulesJson"
        )  # type: Optional[str]
    else:
        system_rules_json_from_obj = None

    return V1SentinelConfig(
        circuitbreaker_rules_json=circuitbreaker_rules_json_from_obj,
        flow_rules_json=flow_rules_json_from_obj,
        isolation_rules_json=isolation_rules_json_from_obj,
        system_rules_json=system_rules_json_from_obj,
    )


def v1_sentinel_config_to_jsonable(
    v1_sentinel_config: V1SentinelConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1SentinelConfig.

    :param v1_sentinel_config: instance of V1SentinelConfig to be JSON-ized
    :param path: path to the v1_sentinel_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_sentinel_config.circuitbreaker_rules_json is not None:
        res["circuitbreakerRulesJson"] = v1_sentinel_config.circuitbreaker_rules_json

    if v1_sentinel_config.flow_rules_json is not None:
        res["flowRulesJson"] = v1_sentinel_config.flow_rules_json

    if v1_sentinel_config.isolation_rules_json is not None:
        res["isolationRulesJson"] = v1_sentinel_config.isolation_rules_json

    if v1_sentinel_config.system_rules_json is not None:
        res["systemRulesJson"] = v1_sentinel_config.system_rules_json

    return res


class V1ServiceConfig:
    """ServiceConfig represents a configuration for a given Stanza SDK instrumented service."""

    def __init__(
        self,
        customer_id: Optional[str] = None,
        trace_config: Optional["V1TraceConfig"] = None,
        metric_config: Optional["V1MetricConfig"] = None,
        sentinel_config: Optional["V1SentinelConfig"] = None,
    ) -> None:
        """Initializes with the given values."""
        self.customer_id = customer_id

        self.trace_config = trace_config

        self.metric_config = metric_config

        self.sentinel_config = sentinel_config

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_service_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_service_config_to_jsonable(self)


def new_v1_service_config() -> V1ServiceConfig:
    """Generates an instance of V1ServiceConfig with default values."""
    return V1ServiceConfig()


def v1_service_config_from_obj(obj: Any, path: str = "") -> V1ServiceConfig:
    """
    Generates an instance of V1ServiceConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1ServiceConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1ServiceConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_customer_id = obj.get("customerId", None)
    if obj_customer_id is not None:
        customer_id_from_obj = from_obj(
            obj_customer_id, expected=[str], path=path + ".customerId"
        )  # type: Optional[str]
    else:
        customer_id_from_obj = None

    obj_trace_config = obj.get("traceConfig", None)
    if obj_trace_config is not None:
        trace_config_from_obj = from_obj(
            obj_trace_config, expected=[V1TraceConfig], path=path + ".traceConfig"
        )  # type: Optional['V1TraceConfig']
    else:
        trace_config_from_obj = None

    obj_metric_config = obj.get("metricConfig", None)
    if obj_metric_config is not None:
        metric_config_from_obj = from_obj(
            obj_metric_config, expected=[V1MetricConfig], path=path + ".metricConfig"
        )  # type: Optional['V1MetricConfig']
    else:
        metric_config_from_obj = None

    obj_sentinel_config = obj.get("sentinelConfig", None)
    if obj_sentinel_config is not None:
        sentinel_config_from_obj = from_obj(
            obj_sentinel_config,
            expected=[V1SentinelConfig],
            path=path + ".sentinelConfig",
        )  # type: Optional['V1SentinelConfig']
    else:
        sentinel_config_from_obj = None

    return V1ServiceConfig(
        customer_id=customer_id_from_obj,
        trace_config=trace_config_from_obj,
        metric_config=metric_config_from_obj,
        sentinel_config=sentinel_config_from_obj,
    )


def v1_service_config_to_jsonable(
    v1_service_config: V1ServiceConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1ServiceConfig.

    :param v1_service_config: instance of V1ServiceConfig to be JSON-ized
    :param path: path to the v1_service_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_service_config.customer_id is not None:
        res["customerId"] = v1_service_config.customer_id

    if v1_service_config.trace_config is not None:
        res["traceConfig"] = to_jsonable(
            v1_service_config.trace_config,
            expected=[V1TraceConfig],
            path="{}.traceConfig".format(path),
        )

    if v1_service_config.metric_config is not None:
        res["metricConfig"] = to_jsonable(
            v1_service_config.metric_config,
            expected=[V1MetricConfig],
            path="{}.metricConfig".format(path),
        )

    if v1_service_config.sentinel_config is not None:
        res["sentinelConfig"] = to_jsonable(
            v1_service_config.sentinel_config,
            expected=[V1SentinelConfig],
            path="{}.sentinelConfig".format(path),
        )

    return res


class V1ServiceSelector:
    def __init__(
        self,
        environment: str,
        name: str,
        release: Optional[str] = None,
        tags: Optional[List["Hubv1Tag"]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.environment = environment

        self.name = name

        self.release = release

        self.tags = tags

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_service_selector_to_jsonable.

        :return: JSON-able representation
        """
        return v1_service_selector_to_jsonable(self)


def new_v1_service_selector() -> V1ServiceSelector:
    """Generates an instance of V1ServiceSelector with default values."""
    return V1ServiceSelector(environment="", name="")


def v1_service_selector_from_obj(obj: Any, path: str = "") -> V1ServiceSelector:
    """
    Generates an instance of V1ServiceSelector from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1ServiceSelector
    :param path: path to the object used for debugging
    :return: parsed instance of V1ServiceSelector
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    environment_from_obj = from_obj(
        obj["environment"], expected=[str], path=path + ".environment"
    )  # type: str

    name_from_obj = from_obj(
        obj["name"], expected=[str], path=path + ".name"
    )  # type: str

    obj_release = obj.get("release", None)
    if obj_release is not None:
        release_from_obj = from_obj(
            obj_release, expected=[str], path=path + ".release"
        )  # type: Optional[str]
    else:
        release_from_obj = None

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    return V1ServiceSelector(
        environment=environment_from_obj,
        name=name_from_obj,
        release=release_from_obj,
        tags=tags_from_obj,
    )


def v1_service_selector_to_jsonable(
    v1_service_selector: V1ServiceSelector, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1ServiceSelector.

    :param v1_service_selector: instance of V1ServiceSelector to be JSON-ized
    :param path: path to the v1_service_selector used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["environment"] = v1_service_selector.environment

    res["name"] = v1_service_selector.name

    if v1_service_selector.release is not None:
        res["release"] = v1_service_selector.release

    if v1_service_selector.tags is not None:
        res["tags"] = to_jsonable(
            v1_service_selector.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    return res


class V1SetTokenLeaseConsumedRequest:
    """Notifies Hub that one or more token leases has been used, i.e. Guard has been exercised."""

    def __init__(
        self,
        tokens: List[str],
        weight_correction: Optional[float] = None,
        environment: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        self.tokens = tokens

        # Used for request weighting, i.e. accounting for varying request sizes and costs. If weights are not known before request execution, then a default or estimated weight may be used, followed by a corrected value here. If a value is sent here, it should be the actual request weight.
        self.weight_correction = weight_correction

        # Must be specified.
        self.environment = environment

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_set_token_lease_consumed_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_set_token_lease_consumed_request_to_jsonable(self)


def new_v1_set_token_lease_consumed_request() -> V1SetTokenLeaseConsumedRequest:
    """Generates an instance of V1SetTokenLeaseConsumedRequest with default values."""
    return V1SetTokenLeaseConsumedRequest(tokens=[])


def v1_set_token_lease_consumed_request_from_obj(
    obj: Any, path: str = ""
) -> V1SetTokenLeaseConsumedRequest:
    """
    Generates an instance of V1SetTokenLeaseConsumedRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1SetTokenLeaseConsumedRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1SetTokenLeaseConsumedRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    tokens_from_obj = from_obj(
        obj["tokens"], expected=[list, str], path=path + ".tokens"
    )  # type: List[str]

    obj_weight_correction = obj.get("weightCorrection", None)
    if obj_weight_correction is not None:
        weight_correction_from_obj = from_obj(
            obj_weight_correction, expected=[float], path=path + ".weightCorrection"
        )  # type: Optional[float]
    else:
        weight_correction_from_obj = None

    obj_environment = obj.get("environment", None)
    if obj_environment is not None:
        environment_from_obj = from_obj(
            obj_environment, expected=[str], path=path + ".environment"
        )  # type: Optional[str]
    else:
        environment_from_obj = None

    return V1SetTokenLeaseConsumedRequest(
        tokens=tokens_from_obj,
        weight_correction=weight_correction_from_obj,
        environment=environment_from_obj,
    )


def v1_set_token_lease_consumed_request_to_jsonable(
    v1_set_token_lease_consumed_request: V1SetTokenLeaseConsumedRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1SetTokenLeaseConsumedRequest.

    :param v1_set_token_lease_consumed_request: instance of V1SetTokenLeaseConsumedRequest to be JSON-ized
    :param path: path to the v1_set_token_lease_consumed_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["tokens"] = to_jsonable(
        v1_set_token_lease_consumed_request.tokens,
        expected=[list, str],
        path="{}.tokens".format(path),
    )

    if v1_set_token_lease_consumed_request.weight_correction is not None:
        res["weightCorrection"] = v1_set_token_lease_consumed_request.weight_correction

    if v1_set_token_lease_consumed_request.environment is not None:
        res["environment"] = v1_set_token_lease_consumed_request.environment

    return res


class V1SetTokenLeaseConsumedResponse:
    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_set_token_lease_consumed_response_to_jsonable.

        :return: a JSON-able representation
        """
        return v1_set_token_lease_consumed_response_to_jsonable(self)


def new_v1_set_token_lease_consumed_response() -> V1SetTokenLeaseConsumedResponse:
    """Generates an instance of V1SetTokenLeaseConsumedResponse with default values."""
    return V1SetTokenLeaseConsumedResponse()


def v1_set_token_lease_consumed_response_from_obj(
    obj: Any, path: str = ""
) -> V1SetTokenLeaseConsumedResponse:
    """
    Generates an instance of V1SetTokenLeaseConsumedResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1SetTokenLeaseConsumedResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1SetTokenLeaseConsumedResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    return V1SetTokenLeaseConsumedResponse()


def v1_set_token_lease_consumed_response_to_jsonable(
    v1_set_token_lease_consumed_response: V1SetTokenLeaseConsumedResponse,
    path: str = "",
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1SetTokenLeaseConsumedResponse.

    :param v1_set_token_lease_consumed_response: instance of V1SetTokenLeaseConsumedResponse to be JSON-ized
    :param path: path to the v1_set_token_lease_consumed_response used for debugging
    :return: a JSON-able representation
    """
    return dict()


class V1SpanSelector:
    def __init__(
        self, otel_attribute: Optional[str] = None, value: Optional[str] = None
    ) -> None:
        """Initializes with the given values."""
        self.otel_attribute = otel_attribute

        # Selector matches if value of 'otel_attribute' equals 'value'.
        self.value = value

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_span_selector_to_jsonable.

        :return: JSON-able representation
        """
        return v1_span_selector_to_jsonable(self)


def new_v1_span_selector() -> V1SpanSelector:
    """Generates an instance of V1SpanSelector with default values."""
    return V1SpanSelector()


def v1_span_selector_from_obj(obj: Any, path: str = "") -> V1SpanSelector:
    """
    Generates an instance of V1SpanSelector from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1SpanSelector
    :param path: path to the object used for debugging
    :return: parsed instance of V1SpanSelector
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_otel_attribute = obj.get("otelAttribute", None)
    if obj_otel_attribute is not None:
        otel_attribute_from_obj = from_obj(
            obj_otel_attribute, expected=[str], path=path + ".otelAttribute"
        )  # type: Optional[str]
    else:
        otel_attribute_from_obj = None

    obj_value = obj.get("value", None)
    if obj_value is not None:
        value_from_obj = from_obj(
            obj_value, expected=[str], path=path + ".value"
        )  # type: Optional[str]
    else:
        value_from_obj = None

    return V1SpanSelector(otel_attribute=otel_attribute_from_obj, value=value_from_obj)


def v1_span_selector_to_jsonable(
    v1_span_selector: V1SpanSelector, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1SpanSelector.

    :param v1_span_selector: instance of V1SpanSelector to be JSON-ized
    :param path: path to the v1_span_selector used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_span_selector.otel_attribute is not None:
        res["otelAttribute"] = v1_span_selector.otel_attribute

    if v1_span_selector.value is not None:
        res["value"] = v1_span_selector.value

    return res


class V1StreamRequest:
    def __init__(
        self,
        stream_id: str,
        max_weight: float,
        min_weight: float,
        feature: Optional[str] = None,
        tags: Optional[List["Hubv1Tag"]] = None,
        priority_boost: Optional[int] = None,
    ) -> None:
        """Initializes with the given values."""
        # Unique identifier for this stream - may be meaningful or a UUID. Assigned by requestor.
        self.stream_id = stream_id

        self.max_weight = max_weight

        # Minimum weight that may be allocated to this stream. If this weight cannot be allocated then the stream cannot be served.
        self.min_weight = min_weight

        self.feature = feature

        self.tags = tags

        # optional - allows priority to be increased or reduced relative to normal default or feature priority.
        self.priority_boost = priority_boost

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_stream_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_stream_request_to_jsonable(self)


def new_v1_stream_request() -> V1StreamRequest:
    """Generates an instance of V1StreamRequest with default values."""
    return V1StreamRequest(stream_id="", max_weight=0.0, min_weight=0.0)


def v1_stream_request_from_obj(obj: Any, path: str = "") -> V1StreamRequest:
    """
    Generates an instance of V1StreamRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1StreamRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1StreamRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    stream_id_from_obj = from_obj(
        obj["streamId"], expected=[str], path=path + ".streamId"
    )  # type: str

    max_weight_from_obj = from_obj(
        obj["maxWeight"], expected=[float], path=path + ".maxWeight"
    )  # type: float

    min_weight_from_obj = from_obj(
        obj["minWeight"], expected=[float], path=path + ".minWeight"
    )  # type: float

    obj_feature = obj.get("feature", None)
    if obj_feature is not None:
        feature_from_obj = from_obj(
            obj_feature, expected=[str], path=path + ".feature"
        )  # type: Optional[str]
    else:
        feature_from_obj = None

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    obj_priority_boost = obj.get("priorityBoost", None)
    if obj_priority_boost is not None:
        priority_boost_from_obj = from_obj(
            obj_priority_boost, expected=[int], path=path + ".priorityBoost"
        )  # type: Optional[int]
    else:
        priority_boost_from_obj = None

    return V1StreamRequest(
        stream_id=stream_id_from_obj,
        max_weight=max_weight_from_obj,
        min_weight=min_weight_from_obj,
        feature=feature_from_obj,
        tags=tags_from_obj,
        priority_boost=priority_boost_from_obj,
    )


def v1_stream_request_to_jsonable(
    v1_stream_request: V1StreamRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1StreamRequest.

    :param v1_stream_request: instance of V1StreamRequest to be JSON-ized
    :param path: path to the v1_stream_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["streamId"] = v1_stream_request.stream_id

    res["maxWeight"] = v1_stream_request.max_weight

    res["minWeight"] = v1_stream_request.min_weight

    if v1_stream_request.feature is not None:
        res["feature"] = v1_stream_request.feature

    if v1_stream_request.tags is not None:
        res["tags"] = to_jsonable(
            v1_stream_request.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    if v1_stream_request.priority_boost is not None:
        res["priorityBoost"] = v1_stream_request.priority_boost

    return res


class V1StreamResult:
    def __init__(
        self, stream_id: str, allocated_weight: Optional[float] = None
    ) -> None:
        """Initializes with the given values."""
        # Unique identifier for this stream - as described in StreamRequest message.
        self.stream_id = stream_id

        # Weight allocated to this stream. Zero means it was not allocated.
        self.allocated_weight = allocated_weight

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_stream_result_to_jsonable.

        :return: JSON-able representation
        """
        return v1_stream_result_to_jsonable(self)


def new_v1_stream_result() -> V1StreamResult:
    """Generates an instance of V1StreamResult with default values."""
    return V1StreamResult(stream_id="")


def v1_stream_result_from_obj(obj: Any, path: str = "") -> V1StreamResult:
    """
    Generates an instance of V1StreamResult from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1StreamResult
    :param path: path to the object used for debugging
    :return: parsed instance of V1StreamResult
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    stream_id_from_obj = from_obj(
        obj["streamId"], expected=[str], path=path + ".streamId"
    )  # type: str

    obj_allocated_weight = obj.get("allocatedWeight", None)
    if obj_allocated_weight is not None:
        allocated_weight_from_obj = from_obj(
            obj_allocated_weight, expected=[float], path=path + ".allocatedWeight"
        )  # type: Optional[float]
    else:
        allocated_weight_from_obj = None

    return V1StreamResult(
        stream_id=stream_id_from_obj, allocated_weight=allocated_weight_from_obj
    )


def v1_stream_result_to_jsonable(
    v1_stream_result: V1StreamResult, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1StreamResult.

    :param v1_stream_result: instance of V1StreamResult to be JSON-ized
    :param path: path to the v1_stream_result used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["streamId"] = v1_stream_result.stream_id

    if v1_stream_result.allocated_weight is not None:
        res["allocatedWeight"] = v1_stream_result.allocated_weight

    return res


class V1TokenInfo:
    def __init__(self, token: str, guard: Optional["V1GuardSelector"] = None) -> None:
        """Initializes with the given values."""
        self.token = token

        self.guard = guard

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_token_info_to_jsonable.

        :return: JSON-able representation
        """
        return v1_token_info_to_jsonable(self)


def new_v1_token_info() -> V1TokenInfo:
    """Generates an instance of V1TokenInfo with default values."""
    return V1TokenInfo(token="")


def v1_token_info_from_obj(obj: Any, path: str = "") -> V1TokenInfo:
    """
    Generates an instance of V1TokenInfo from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1TokenInfo
    :param path: path to the object used for debugging
    :return: parsed instance of V1TokenInfo
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    token_from_obj = from_obj(
        obj["token"], expected=[str], path=path + ".token"
    )  # type: str

    obj_guard = obj.get("guard", None)
    if obj_guard is not None:
        guard_from_obj = from_obj(
            obj_guard, expected=[V1GuardSelector], path=path + ".guard"
        )  # type: Optional['V1GuardSelector']
    else:
        guard_from_obj = None

    return V1TokenInfo(token=token_from_obj, guard=guard_from_obj)


def v1_token_info_to_jsonable(
    v1_token_info: V1TokenInfo, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1TokenInfo.

    :param v1_token_info: instance of V1TokenInfo to be JSON-ized
    :param path: path to the v1_token_info used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["token"] = v1_token_info.token

    if v1_token_info.guard is not None:
        res["guard"] = to_jsonable(
            v1_token_info.guard,
            expected=[V1GuardSelector],
            path="{}.guard".format(path),
        )

    return res


class V1TokenLease:
    def __init__(
        self,
        duration_msec: Optional[int] = None,
        token: Optional[str] = None,
        feature: Optional[str] = None,
        priority_boost: Optional[int] = None,
        weight: Optional[float] = None,
        reason: Optional[str] = None,
        expires_at: Optional[str] = None,
        mode: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        self.duration_msec = duration_msec

        self.token = token

        self.feature = feature

        self.priority_boost = priority_boost

        self.weight = weight

        self.reason = reason

        self.expires_at = expires_at

        self.mode = mode

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_token_lease_to_jsonable.

        :return: JSON-able representation
        """
        return v1_token_lease_to_jsonable(self)


def new_v1_token_lease() -> V1TokenLease:
    """Generates an instance of V1TokenLease with default values."""
    return V1TokenLease()


def v1_token_lease_from_obj(obj: Any, path: str = "") -> V1TokenLease:
    """
    Generates an instance of V1TokenLease from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1TokenLease
    :param path: path to the object used for debugging
    :return: parsed instance of V1TokenLease
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_duration_msec = obj.get("durationMsec", None)
    if obj_duration_msec is not None:
        duration_msec_from_obj = from_obj(
            obj_duration_msec, expected=[int], path=path + ".durationMsec"
        )  # type: Optional[int]
    else:
        duration_msec_from_obj = None

    obj_token = obj.get("token", None)
    if obj_token is not None:
        token_from_obj = from_obj(
            obj_token, expected=[str], path=path + ".token"
        )  # type: Optional[str]
    else:
        token_from_obj = None

    obj_feature = obj.get("feature", None)
    if obj_feature is not None:
        feature_from_obj = from_obj(
            obj_feature, expected=[str], path=path + ".feature"
        )  # type: Optional[str]
    else:
        feature_from_obj = None

    obj_priority_boost = obj.get("priorityBoost", None)
    if obj_priority_boost is not None:
        priority_boost_from_obj = from_obj(
            obj_priority_boost, expected=[int], path=path + ".priorityBoost"
        )  # type: Optional[int]
    else:
        priority_boost_from_obj = None

    obj_weight = obj.get("weight", None)
    if obj_weight is not None:
        weight_from_obj = from_obj(
            obj_weight, expected=[float], path=path + ".weight"
        )  # type: Optional[float]
    else:
        weight_from_obj = None

    obj_reason = obj.get("reason", None)
    if obj_reason is not None:
        reason_from_obj = from_obj(
            obj_reason, expected=[str], path=path + ".reason"
        )  # type: Optional[str]
    else:
        reason_from_obj = None

    obj_expires_at = obj.get("expiresAt", None)
    if obj_expires_at is not None:
        expires_at_from_obj = from_obj(
            obj_expires_at, expected=[str], path=path + ".expiresAt"
        )  # type: Optional[str]
    else:
        expires_at_from_obj = None

    obj_mode = obj.get("mode", None)
    if obj_mode is not None:
        mode_from_obj = from_obj(
            obj_mode, expected=[str], path=path + ".mode"
        )  # type: Optional[str]
    else:
        mode_from_obj = None

    return V1TokenLease(
        duration_msec=duration_msec_from_obj,
        token=token_from_obj,
        feature=feature_from_obj,
        priority_boost=priority_boost_from_obj,
        weight=weight_from_obj,
        reason=reason_from_obj,
        expires_at=expires_at_from_obj,
        mode=mode_from_obj,
    )


def v1_token_lease_to_jsonable(
    v1_token_lease: V1TokenLease, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1TokenLease.

    :param v1_token_lease: instance of V1TokenLease to be JSON-ized
    :param path: path to the v1_token_lease used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_token_lease.duration_msec is not None:
        res["durationMsec"] = v1_token_lease.duration_msec

    if v1_token_lease.token is not None:
        res["token"] = v1_token_lease.token

    if v1_token_lease.feature is not None:
        res["feature"] = v1_token_lease.feature

    if v1_token_lease.priority_boost is not None:
        res["priorityBoost"] = v1_token_lease.priority_boost

    if v1_token_lease.weight is not None:
        res["weight"] = v1_token_lease.weight

    if v1_token_lease.reason is not None:
        res["reason"] = v1_token_lease.reason

    if v1_token_lease.expires_at is not None:
        res["expiresAt"] = v1_token_lease.expires_at

    if v1_token_lease.mode is not None:
        res["mode"] = v1_token_lease.mode

    return res


class V1TokenValid:
    def __init__(
        self, token: Optional[str] = None, valid: Optional[bool] = None
    ) -> None:
        """Initializes with the given values."""
        self.token = token

        self.valid = valid

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_token_valid_to_jsonable.

        :return: JSON-able representation
        """
        return v1_token_valid_to_jsonable(self)


def new_v1_token_valid() -> V1TokenValid:
    """Generates an instance of V1TokenValid with default values."""
    return V1TokenValid()


def v1_token_valid_from_obj(obj: Any, path: str = "") -> V1TokenValid:
    """
    Generates an instance of V1TokenValid from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1TokenValid
    :param path: path to the object used for debugging
    :return: parsed instance of V1TokenValid
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_token = obj.get("token", None)
    if obj_token is not None:
        token_from_obj = from_obj(
            obj_token, expected=[str], path=path + ".token"
        )  # type: Optional[str]
    else:
        token_from_obj = None

    obj_valid = obj.get("valid", None)
    if obj_valid is not None:
        valid_from_obj = from_obj(
            obj_valid, expected=[bool], path=path + ".valid"
        )  # type: Optional[bool]
    else:
        valid_from_obj = None

    return V1TokenValid(token=token_from_obj, valid=valid_from_obj)


def v1_token_valid_to_jsonable(
    v1_token_valid: V1TokenValid, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1TokenValid.

    :param v1_token_valid: instance of V1TokenValid to be JSON-ized
    :param path: path to the v1_token_valid used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_token_valid.token is not None:
        res["token"] = v1_token_valid.token

    if v1_token_valid.valid is not None:
        res["valid"] = v1_token_valid.valid

    return res


class V1TraceConfig:
    def __init__(
        self,
        collector_url: Optional[str] = None,
        sample_rate_default: Optional[float] = None,
        overrides: Optional[List["V1TraceConfigOverride"]] = None,
        header_sample_configs: Optional[List["V1HeaderTraceConfig"]] = None,
        param_sample_configs: Optional[List["V1ParamTraceConfig"]] = None,
    ) -> None:
        """Initializes with the given values."""
        # URL of OTEL trace collector. If URL begins with http or https it will be treated as an HTTP collector, otherwise it will be treated as a gRPC collector.
        self.collector_url = collector_url

        self.sample_rate_default = sample_rate_default

        self.overrides = overrides

        self.header_sample_configs = header_sample_configs

        self.param_sample_configs = param_sample_configs

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_trace_config_to_jsonable.

        :return: JSON-able representation
        """
        return v1_trace_config_to_jsonable(self)


def new_v1_trace_config() -> V1TraceConfig:
    """Generates an instance of V1TraceConfig with default values."""
    return V1TraceConfig()


def v1_trace_config_from_obj(obj: Any, path: str = "") -> V1TraceConfig:
    """
    Generates an instance of V1TraceConfig from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1TraceConfig
    :param path: path to the object used for debugging
    :return: parsed instance of V1TraceConfig
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_collector_url = obj.get("collectorUrl", None)
    if obj_collector_url is not None:
        collector_url_from_obj = from_obj(
            obj_collector_url, expected=[str], path=path + ".collectorUrl"
        )  # type: Optional[str]
    else:
        collector_url_from_obj = None

    obj_sample_rate_default = obj.get("sampleRateDefault", None)
    if obj_sample_rate_default is not None:
        sample_rate_default_from_obj = from_obj(
            obj_sample_rate_default, expected=[float], path=path + ".sampleRateDefault"
        )  # type: Optional[float]
    else:
        sample_rate_default_from_obj = None

    obj_overrides = obj.get("overrides", None)
    if obj_overrides is not None:
        overrides_from_obj = from_obj(
            obj_overrides,
            expected=[list, V1TraceConfigOverride],
            path=path + ".overrides",
        )  # type: Optional[List['V1TraceConfigOverride']]
    else:
        overrides_from_obj = None

    obj_header_sample_configs = obj.get("headerSampleConfigs", None)
    if obj_header_sample_configs is not None:
        header_sample_configs_from_obj = from_obj(
            obj_header_sample_configs,
            expected=[list, V1HeaderTraceConfig],
            path=path + ".headerSampleConfigs",
        )  # type: Optional[List['V1HeaderTraceConfig']]
    else:
        header_sample_configs_from_obj = None

    obj_param_sample_configs = obj.get("paramSampleConfigs", None)
    if obj_param_sample_configs is not None:
        param_sample_configs_from_obj = from_obj(
            obj_param_sample_configs,
            expected=[list, V1ParamTraceConfig],
            path=path + ".paramSampleConfigs",
        )  # type: Optional[List['V1ParamTraceConfig']]
    else:
        param_sample_configs_from_obj = None

    return V1TraceConfig(
        collector_url=collector_url_from_obj,
        sample_rate_default=sample_rate_default_from_obj,
        overrides=overrides_from_obj,
        header_sample_configs=header_sample_configs_from_obj,
        param_sample_configs=param_sample_configs_from_obj,
    )


def v1_trace_config_to_jsonable(
    v1_trace_config: V1TraceConfig, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1TraceConfig.

    :param v1_trace_config: instance of V1TraceConfig to be JSON-ized
    :param path: path to the v1_trace_config used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_trace_config.collector_url is not None:
        res["collectorUrl"] = v1_trace_config.collector_url

    if v1_trace_config.sample_rate_default is not None:
        res["sampleRateDefault"] = v1_trace_config.sample_rate_default

    if v1_trace_config.overrides is not None:
        res["overrides"] = to_jsonable(
            v1_trace_config.overrides,
            expected=[list, V1TraceConfigOverride],
            path="{}.overrides".format(path),
        )

    if v1_trace_config.header_sample_configs is not None:
        res["headerSampleConfigs"] = to_jsonable(
            v1_trace_config.header_sample_configs,
            expected=[list, V1HeaderTraceConfig],
            path="{}.headerSampleConfigs".format(path),
        )

    if v1_trace_config.param_sample_configs is not None:
        res["paramSampleConfigs"] = to_jsonable(
            v1_trace_config.param_sample_configs,
            expected=[list, V1ParamTraceConfig],
            path="{}.paramSampleConfigs".format(path),
        )

    return res


class V1TraceConfigOverride:
    """This configuration allows different sample rates to be applied to selected spans."""

    def __init__(
        self,
        sample_rate: Optional[float] = None,
        span_selectors: Optional[List["V1SpanSelector"]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.sample_rate = sample_rate

        self.span_selectors = span_selectors

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_trace_config_override_to_jsonable.

        :return: JSON-able representation
        """
        return v1_trace_config_override_to_jsonable(self)


def new_v1_trace_config_override() -> V1TraceConfigOverride:
    """Generates an instance of V1TraceConfigOverride with default values."""
    return V1TraceConfigOverride()


def v1_trace_config_override_from_obj(
    obj: Any, path: str = ""
) -> V1TraceConfigOverride:
    """
    Generates an instance of V1TraceConfigOverride from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1TraceConfigOverride
    :param path: path to the object used for debugging
    :return: parsed instance of V1TraceConfigOverride
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_sample_rate = obj.get("sampleRate", None)
    if obj_sample_rate is not None:
        sample_rate_from_obj = from_obj(
            obj_sample_rate, expected=[float], path=path + ".sampleRate"
        )  # type: Optional[float]
    else:
        sample_rate_from_obj = None

    obj_span_selectors = obj.get("spanSelectors", None)
    if obj_span_selectors is not None:
        span_selectors_from_obj = from_obj(
            obj_span_selectors,
            expected=[list, V1SpanSelector],
            path=path + ".spanSelectors",
        )  # type: Optional[List['V1SpanSelector']]
    else:
        span_selectors_from_obj = None

    return V1TraceConfigOverride(
        sample_rate=sample_rate_from_obj, span_selectors=span_selectors_from_obj
    )


def v1_trace_config_override_to_jsonable(
    v1_trace_config_override: V1TraceConfigOverride, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1TraceConfigOverride.

    :param v1_trace_config_override: instance of V1TraceConfigOverride to be JSON-ized
    :param path: path to the v1_trace_config_override used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_trace_config_override.sample_rate is not None:
        res["sampleRate"] = v1_trace_config_override.sample_rate

    if v1_trace_config_override.span_selectors is not None:
        res["spanSelectors"] = to_jsonable(
            v1_trace_config_override.span_selectors,
            expected=[list, V1SpanSelector],
            path="{}.spanSelectors".format(path),
        )

    return res


class V1UpdateStreamsRequest:
    def __init__(
        self,
        guard_name: str,
        environment: str,
        requests: Optional[List["V1StreamRequest"]] = None,
        ended: Optional[List[str]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.guard_name = guard_name

        self.environment = environment

        self.requests = requests

        self.ended = ended

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_update_streams_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_update_streams_request_to_jsonable(self)


def new_v1_update_streams_request() -> V1UpdateStreamsRequest:
    """Generates an instance of V1UpdateStreamsRequest with default values."""
    return V1UpdateStreamsRequest(guard_name="", environment="")


def v1_update_streams_request_from_obj(
    obj: Any, path: str = ""
) -> V1UpdateStreamsRequest:
    """
    Generates an instance of V1UpdateStreamsRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1UpdateStreamsRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1UpdateStreamsRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    guard_name_from_obj = from_obj(
        obj["guardName"], expected=[str], path=path + ".guardName"
    )  # type: str

    environment_from_obj = from_obj(
        obj["environment"], expected=[str], path=path + ".environment"
    )  # type: str

    obj_requests = obj.get("requests", None)
    if obj_requests is not None:
        requests_from_obj = from_obj(
            obj_requests, expected=[list, V1StreamRequest], path=path + ".requests"
        )  # type: Optional[List['V1StreamRequest']]
    else:
        requests_from_obj = None

    obj_ended = obj.get("ended", None)
    if obj_ended is not None:
        ended_from_obj = from_obj(
            obj_ended, expected=[list, str], path=path + ".ended"
        )  # type: Optional[List[str]]
    else:
        ended_from_obj = None

    return V1UpdateStreamsRequest(
        guard_name=guard_name_from_obj,
        environment=environment_from_obj,
        requests=requests_from_obj,
        ended=ended_from_obj,
    )


def v1_update_streams_request_to_jsonable(
    v1_update_streams_request: V1UpdateStreamsRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1UpdateStreamsRequest.

    :param v1_update_streams_request: instance of V1UpdateStreamsRequest to be JSON-ized
    :param path: path to the v1_update_streams_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    res["guardName"] = v1_update_streams_request.guard_name

    res["environment"] = v1_update_streams_request.environment

    if v1_update_streams_request.requests is not None:
        res["requests"] = to_jsonable(
            v1_update_streams_request.requests,
            expected=[list, V1StreamRequest],
            path="{}.requests".format(path),
        )

    if v1_update_streams_request.ended is not None:
        res["ended"] = to_jsonable(
            v1_update_streams_request.ended,
            expected=[list, str],
            path="{}.ended".format(path),
        )

    return res


class V1UpdateStreamsResponse:
    def __init__(self, results: Optional[List["V1StreamResult"]] = None) -> None:
        """Initializes with the given values."""
        self.results = results

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_update_streams_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_update_streams_response_to_jsonable(self)


def new_v1_update_streams_response() -> V1UpdateStreamsResponse:
    """Generates an instance of V1UpdateStreamsResponse with default values."""
    return V1UpdateStreamsResponse()


def v1_update_streams_response_from_obj(
    obj: Any, path: str = ""
) -> V1UpdateStreamsResponse:
    """
    Generates an instance of V1UpdateStreamsResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1UpdateStreamsResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1UpdateStreamsResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_results = obj.get("results", None)
    if obj_results is not None:
        results_from_obj = from_obj(
            obj_results, expected=[list, V1StreamResult], path=path + ".results"
        )  # type: Optional[List['V1StreamResult']]
    else:
        results_from_obj = None

    return V1UpdateStreamsResponse(results=results_from_obj)


def v1_update_streams_response_to_jsonable(
    v1_update_streams_response: V1UpdateStreamsResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1UpdateStreamsResponse.

    :param v1_update_streams_response: instance of V1UpdateStreamsResponse to be JSON-ized
    :param path: path to the v1_update_streams_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_update_streams_response.results is not None:
        res["results"] = to_jsonable(
            v1_update_streams_response.results,
            expected=[list, V1StreamResult],
            path="{}.results".format(path),
        )

    return res


class V1UsageTSDataPoint:
    def __init__(
        self,
        start_ts: Optional[str] = None,
        end_ts: Optional[str] = None,
        granted: Optional[int] = None,
        granted_weight: Optional[float] = None,
        not_granted: Optional[int] = None,
        not_granted_weight: Optional[float] = None,
        be_burst: Optional[int] = None,
        be_burst_weight: Optional[float] = None,
        parent_reject: Optional[int] = None,
        parent_reject_weight: Optional[float] = None,
    ) -> None:
        """Initializes with the given values."""
        self.start_ts = start_ts

        self.end_ts = end_ts

        self.granted = granted

        self.granted_weight = granted_weight

        self.not_granted = not_granted

        self.not_granted_weight = not_granted_weight

        self.be_burst = be_burst

        self.be_burst_weight = be_burst_weight

        self.parent_reject = parent_reject

        self.parent_reject_weight = parent_reject_weight

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_usage_t_s_data_point_to_jsonable.

        :return: JSON-able representation
        """
        return v1_usage_t_s_data_point_to_jsonable(self)


def new_v1_usage_t_s_data_point() -> V1UsageTSDataPoint:
    """Generates an instance of V1UsageTSDataPoint with default values."""
    return V1UsageTSDataPoint()


def v1_usage_t_s_data_point_from_obj(obj: Any, path: str = "") -> V1UsageTSDataPoint:
    """
    Generates an instance of V1UsageTSDataPoint from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1UsageTSDataPoint
    :param path: path to the object used for debugging
    :return: parsed instance of V1UsageTSDataPoint
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_start_ts = obj.get("startTs", None)
    if obj_start_ts is not None:
        start_ts_from_obj = from_obj(
            obj_start_ts, expected=[str], path=path + ".startTs"
        )  # type: Optional[str]
    else:
        start_ts_from_obj = None

    obj_end_ts = obj.get("endTs", None)
    if obj_end_ts is not None:
        end_ts_from_obj = from_obj(
            obj_end_ts, expected=[str], path=path + ".endTs"
        )  # type: Optional[str]
    else:
        end_ts_from_obj = None

    obj_granted = obj.get("granted", None)
    if obj_granted is not None:
        granted_from_obj = from_obj(
            obj_granted, expected=[int], path=path + ".granted"
        )  # type: Optional[int]
    else:
        granted_from_obj = None

    obj_granted_weight = obj.get("grantedWeight", None)
    if obj_granted_weight is not None:
        granted_weight_from_obj = from_obj(
            obj_granted_weight, expected=[float], path=path + ".grantedWeight"
        )  # type: Optional[float]
    else:
        granted_weight_from_obj = None

    obj_not_granted = obj.get("notGranted", None)
    if obj_not_granted is not None:
        not_granted_from_obj = from_obj(
            obj_not_granted, expected=[int], path=path + ".notGranted"
        )  # type: Optional[int]
    else:
        not_granted_from_obj = None

    obj_not_granted_weight = obj.get("notGrantedWeight", None)
    if obj_not_granted_weight is not None:
        not_granted_weight_from_obj = from_obj(
            obj_not_granted_weight, expected=[float], path=path + ".notGrantedWeight"
        )  # type: Optional[float]
    else:
        not_granted_weight_from_obj = None

    obj_be_burst = obj.get("beBurst", None)
    if obj_be_burst is not None:
        be_burst_from_obj = from_obj(
            obj_be_burst, expected=[int], path=path + ".beBurst"
        )  # type: Optional[int]
    else:
        be_burst_from_obj = None

    obj_be_burst_weight = obj.get("beBurstWeight", None)
    if obj_be_burst_weight is not None:
        be_burst_weight_from_obj = from_obj(
            obj_be_burst_weight, expected=[float], path=path + ".beBurstWeight"
        )  # type: Optional[float]
    else:
        be_burst_weight_from_obj = None

    obj_parent_reject = obj.get("parentReject", None)
    if obj_parent_reject is not None:
        parent_reject_from_obj = from_obj(
            obj_parent_reject, expected=[int], path=path + ".parentReject"
        )  # type: Optional[int]
    else:
        parent_reject_from_obj = None

    obj_parent_reject_weight = obj.get("parentRejectWeight", None)
    if obj_parent_reject_weight is not None:
        parent_reject_weight_from_obj = from_obj(
            obj_parent_reject_weight,
            expected=[float],
            path=path + ".parentRejectWeight",
        )  # type: Optional[float]
    else:
        parent_reject_weight_from_obj = None

    return V1UsageTSDataPoint(
        start_ts=start_ts_from_obj,
        end_ts=end_ts_from_obj,
        granted=granted_from_obj,
        granted_weight=granted_weight_from_obj,
        not_granted=not_granted_from_obj,
        not_granted_weight=not_granted_weight_from_obj,
        be_burst=be_burst_from_obj,
        be_burst_weight=be_burst_weight_from_obj,
        parent_reject=parent_reject_from_obj,
        parent_reject_weight=parent_reject_weight_from_obj,
    )


def v1_usage_t_s_data_point_to_jsonable(
    v1_usage_t_s_data_point: V1UsageTSDataPoint, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1UsageTSDataPoint.

    :param v1_usage_t_s_data_point: instance of V1UsageTSDataPoint to be JSON-ized
    :param path: path to the v1_usage_t_s_data_point used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_usage_t_s_data_point.start_ts is not None:
        res["startTs"] = v1_usage_t_s_data_point.start_ts

    if v1_usage_t_s_data_point.end_ts is not None:
        res["endTs"] = v1_usage_t_s_data_point.end_ts

    if v1_usage_t_s_data_point.granted is not None:
        res["granted"] = v1_usage_t_s_data_point.granted

    if v1_usage_t_s_data_point.granted_weight is not None:
        res["grantedWeight"] = v1_usage_t_s_data_point.granted_weight

    if v1_usage_t_s_data_point.not_granted is not None:
        res["notGranted"] = v1_usage_t_s_data_point.not_granted

    if v1_usage_t_s_data_point.not_granted_weight is not None:
        res["notGrantedWeight"] = v1_usage_t_s_data_point.not_granted_weight

    if v1_usage_t_s_data_point.be_burst is not None:
        res["beBurst"] = v1_usage_t_s_data_point.be_burst

    if v1_usage_t_s_data_point.be_burst_weight is not None:
        res["beBurstWeight"] = v1_usage_t_s_data_point.be_burst_weight

    if v1_usage_t_s_data_point.parent_reject is not None:
        res["parentReject"] = v1_usage_t_s_data_point.parent_reject

    if v1_usage_t_s_data_point.parent_reject_weight is not None:
        res["parentRejectWeight"] = v1_usage_t_s_data_point.parent_reject_weight

    return res


class V1UsageTimeseries:
    def __init__(
        self,
        data: Optional[List["V1UsageTSDataPoint"]] = None,
        feature: Optional[str] = None,
        priority: Optional[int] = None,
        tags: Optional[List["Hubv1Tag"]] = None,
        guard: Optional[str] = None,
        service: Optional[str] = None,
    ) -> None:
        """Initializes with the given values."""
        self.data = data

        self.feature = feature

        self.priority = priority

        self.tags = tags

        self.guard = guard

        self.service = service

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_usage_timeseries_to_jsonable.

        :return: JSON-able representation
        """
        return v1_usage_timeseries_to_jsonable(self)


def new_v1_usage_timeseries() -> V1UsageTimeseries:
    """Generates an instance of V1UsageTimeseries with default values."""
    return V1UsageTimeseries()


def v1_usage_timeseries_from_obj(obj: Any, path: str = "") -> V1UsageTimeseries:
    """
    Generates an instance of V1UsageTimeseries from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1UsageTimeseries
    :param path: path to the object used for debugging
    :return: parsed instance of V1UsageTimeseries
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_data = obj.get("data", None)
    if obj_data is not None:
        data_from_obj = from_obj(
            obj_data, expected=[list, V1UsageTSDataPoint], path=path + ".data"
        )  # type: Optional[List['V1UsageTSDataPoint']]
    else:
        data_from_obj = None

    obj_feature = obj.get("feature", None)
    if obj_feature is not None:
        feature_from_obj = from_obj(
            obj_feature, expected=[str], path=path + ".feature"
        )  # type: Optional[str]
    else:
        feature_from_obj = None

    obj_priority = obj.get("priority", None)
    if obj_priority is not None:
        priority_from_obj = from_obj(
            obj_priority, expected=[int], path=path + ".priority"
        )  # type: Optional[int]
    else:
        priority_from_obj = None

    obj_tags = obj.get("tags", None)
    if obj_tags is not None:
        tags_from_obj = from_obj(
            obj_tags, expected=[list, Hubv1Tag], path=path + ".tags"
        )  # type: Optional[List['Hubv1Tag']]
    else:
        tags_from_obj = None

    obj_guard = obj.get("guard", None)
    if obj_guard is not None:
        guard_from_obj = from_obj(
            obj_guard, expected=[str], path=path + ".guard"
        )  # type: Optional[str]
    else:
        guard_from_obj = None

    obj_service = obj.get("service", None)
    if obj_service is not None:
        service_from_obj = from_obj(
            obj_service, expected=[str], path=path + ".service"
        )  # type: Optional[str]
    else:
        service_from_obj = None

    return V1UsageTimeseries(
        data=data_from_obj,
        feature=feature_from_obj,
        priority=priority_from_obj,
        tags=tags_from_obj,
        guard=guard_from_obj,
        service=service_from_obj,
    )


def v1_usage_timeseries_to_jsonable(
    v1_usage_timeseries: V1UsageTimeseries, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1UsageTimeseries.

    :param v1_usage_timeseries: instance of V1UsageTimeseries to be JSON-ized
    :param path: path to the v1_usage_timeseries used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_usage_timeseries.data is not None:
        res["data"] = to_jsonable(
            v1_usage_timeseries.data,
            expected=[list, V1UsageTSDataPoint],
            path="{}.data".format(path),
        )

    if v1_usage_timeseries.feature is not None:
        res["feature"] = v1_usage_timeseries.feature

    if v1_usage_timeseries.priority is not None:
        res["priority"] = v1_usage_timeseries.priority

    if v1_usage_timeseries.tags is not None:
        res["tags"] = to_jsonable(
            v1_usage_timeseries.tags,
            expected=[list, Hubv1Tag],
            path="{}.tags".format(path),
        )

    if v1_usage_timeseries.guard is not None:
        res["guard"] = v1_usage_timeseries.guard

    if v1_usage_timeseries.service is not None:
        res["service"] = v1_usage_timeseries.service

    return res


class V1ValidateTokenRequest:
    """Calls Hub to validate a token (ensures token has not expired, was minted by Hub, and related to the specified Guard). Used from Ingress Guards. Ensures callers have acquired quota prior to expending resources."""

    def __init__(self, tokens: Optional[List["V1TokenInfo"]] = None) -> None:
        """Initializes with the given values."""
        self.tokens = tokens

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_validate_token_request_to_jsonable.

        :return: JSON-able representation
        """
        return v1_validate_token_request_to_jsonable(self)


def new_v1_validate_token_request() -> V1ValidateTokenRequest:
    """Generates an instance of V1ValidateTokenRequest with default values."""
    return V1ValidateTokenRequest()


def v1_validate_token_request_from_obj(
    obj: Any, path: str = ""
) -> V1ValidateTokenRequest:
    """
    Generates an instance of V1ValidateTokenRequest from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1ValidateTokenRequest
    :param path: path to the object used for debugging
    :return: parsed instance of V1ValidateTokenRequest
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_tokens = obj.get("tokens", None)
    if obj_tokens is not None:
        tokens_from_obj = from_obj(
            obj_tokens, expected=[list, V1TokenInfo], path=path + ".tokens"
        )  # type: Optional[List['V1TokenInfo']]
    else:
        tokens_from_obj = None

    return V1ValidateTokenRequest(tokens=tokens_from_obj)


def v1_validate_token_request_to_jsonable(
    v1_validate_token_request: V1ValidateTokenRequest, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1ValidateTokenRequest.

    :param v1_validate_token_request: instance of V1ValidateTokenRequest to be JSON-ized
    :param path: path to the v1_validate_token_request used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_validate_token_request.tokens is not None:
        res["tokens"] = to_jsonable(
            v1_validate_token_request.tokens,
            expected=[list, V1TokenInfo],
            path="{}.tokens".format(path),
        )

    return res


class V1ValidateTokenResponse:
    """Specifies whether tokens were valid or not."""

    def __init__(
        self,
        valid: Optional[bool] = None,
        tokens_valid: Optional[List["V1TokenValid"]] = None,
    ) -> None:
        """Initializes with the given values."""
        self.valid = valid

        self.tokens_valid = tokens_valid

    def to_jsonable(self) -> MutableMapping[str, Any]:
        """
        Dispatches the conversion to v1_validate_token_response_to_jsonable.

        :return: JSON-able representation
        """
        return v1_validate_token_response_to_jsonable(self)


def new_v1_validate_token_response() -> V1ValidateTokenResponse:
    """Generates an instance of V1ValidateTokenResponse with default values."""
    return V1ValidateTokenResponse()


def v1_validate_token_response_from_obj(
    obj: Any, path: str = ""
) -> V1ValidateTokenResponse:
    """
    Generates an instance of V1ValidateTokenResponse from a dictionary object.

    :param obj: a JSON-ed dictionary object representing an instance of V1ValidateTokenResponse
    :param path: path to the object used for debugging
    :return: parsed instance of V1ValidateTokenResponse
    """
    if not isinstance(obj, dict):
        raise ValueError(
            "Expected a dict at path {}, but got: {}".format(path, type(obj))
        )

    for key in obj:
        if not isinstance(key, str):
            raise ValueError(
                "Expected a key of type str at path {}, but got: {}".format(
                    path, type(key)
                )
            )

    obj_valid = obj.get("valid", None)
    if obj_valid is not None:
        valid_from_obj = from_obj(
            obj_valid, expected=[bool], path=path + ".valid"
        )  # type: Optional[bool]
    else:
        valid_from_obj = None

    obj_tokens_valid = obj.get("tokensValid", None)
    if obj_tokens_valid is not None:
        tokens_valid_from_obj = from_obj(
            obj_tokens_valid, expected=[list, V1TokenValid], path=path + ".tokensValid"
        )  # type: Optional[List['V1TokenValid']]
    else:
        tokens_valid_from_obj = None

    return V1ValidateTokenResponse(
        valid=valid_from_obj, tokens_valid=tokens_valid_from_obj
    )


def v1_validate_token_response_to_jsonable(
    v1_validate_token_response: V1ValidateTokenResponse, path: str = ""
) -> MutableMapping[str, Any]:
    """
    Generates a JSON-able mapping from an instance of V1ValidateTokenResponse.

    :param v1_validate_token_response: instance of V1ValidateTokenResponse to be JSON-ized
    :param path: path to the v1_validate_token_response used for debugging
    :return: a JSON-able representation
    """
    res = dict()  # type: Dict[str, Any]

    if v1_validate_token_response.valid is not None:
        res["valid"] = v1_validate_token_response.valid

    if v1_validate_token_response.tokens_valid is not None:
        res["tokensValid"] = to_jsonable(
            v1_validate_token_response.tokens_valid,
            expected=[list, V1TokenValid],
            path="{}.tokensValid".format(path),
        )

    return res


class RemoteCaller:
    """Executes the remote calls to the server."""

    def __init__(
        self,
        url_prefix: str,
        auth: Optional[requests.auth.AuthBase] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.url_prefix = url_prefix
        self.auth = auth
        self.session = session

        if not self.session:
            self.session = requests.Session()
            self.session.auth = self.auth

    def auth_service_get_bearer_token(
        self, environment: Optional[str] = None
    ) -> "V1GetBearerTokenResponse":
        """
        Inspects the X-Stanza-Key auth header and returns a new Bearer Token if API key is valid.

        :param environment: Must be specified.

        :return: OK
        """
        url = self.url_prefix + "/v1/auth/token"

        params = {}  # type: Dict[str, str]

        if environment is not None:
            params["environment"] = environment

        resp = self.session.request(
            method="get",
            url=url,
            params=params,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1GetBearerTokenResponse])

    def config_service_get_guard_config(
        self, body: "V1GetGuardConfigRequest"
    ) -> "V1GetGuardConfigResponse":
        """
        Used by SDK to get a Guard Config from Stanza Hub.

        :param body: Request from Backend SDKs for a Guard Config. SDKs are expected to periodically poll, giving the version of the most recent configuration seen. Configurations may be large; we will not re-send them unless they have changed. Guard configurations may vary between environments but are SHARED between Services.

        :return: OK
        """
        url = self.url_prefix + "/v1/config/guard"

        data = to_jsonable(body, expected=[V1GetGuardConfigRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1GetGuardConfigResponse])

    def config_service_get_service_config(
        self, body: "V1GetServiceConfigRequest"
    ) -> "V1GetServiceConfigResponse":
        """
        Used by SDK to get a Service Config from Stanza Hub.

        :param body: The request from Backend SDKs for a Service Config. SDKs are expected to periodically poll, giving the version of the most recent configuration seen. Configurations may be large; we will not re-send them unless they have changed.

        :return: OK
        """
        url = self.url_prefix + "/v1/config/service"

        data = to_jsonable(body, expected=[V1GetServiceConfigRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1GetServiceConfigResponse])

    def config_service_get_browser_context(
        self, body: "V1GetBrowserContextRequest"
    ) -> "V1GetBrowserContextResponse":
        """
        Used by SDK to get a Browser Context from Stanza Hub.

        :param body: The request from Browser SDKs for a Browser Context. SDKs are expected to periodically poll, giving the version of the most recent configuration seen. Configurations may be large; we will not re-send them unless they have changed.

        :return: OK
        """
        url = self.url_prefix + "/v1/context/browser"

        data = to_jsonable(body, expected=[V1GetBrowserContextRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1GetBrowserContextResponse])

    def health_service_query_guard_health(
        self, body: "V1QueryGuardHealthRequest"
    ) -> "V1QueryGuardHealthResponse":
        """
        Used by SDK to allow developers to make decisions about graceful degradation of backend services.

        :param body: Called by SDK to determine whether a Guard is overloaded at a given Feature's priority level. Used so that customer code can make good decisions about fail-fast or graceful degradation as high up the stack as possible. SDK may cache the result for up to 10 seconds.

        :return: OK
        """
        url = self.url_prefix + "/v1/health/guard"

        data = to_jsonable(body, expected=[V1QueryGuardHealthRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1QueryGuardHealthResponse])

    def quota_service_set_token_lease_consumed(
        self, body: "V1SetTokenLeaseConsumedRequest"
    ) -> "V1SetTokenLeaseConsumedResponse":
        """
        Inform Stanza Hub that quota access tokens were consumed.

        :param body: Notifies Hub that one or more token leases has been used, i.e. Guard has been exercised.

        :return: OK
        """
        url = self.url_prefix + "/v1/quota/consumed"

        data = to_jsonable(body, expected=[V1SetTokenLeaseConsumedRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1SetTokenLeaseConsumedResponse])

    def quota_service_get_token_lease(
        self, body: "V1GetTokenLeaseRequest"
    ) -> "V1GetTokenLeaseResponse":
        """
        Get a set of token leases from Stanza Hub for access to given Guard (optional Feature name for priority).

        :param body: Requests token lease for given Guard at priority of specified feature.

        :return: OK
        """
        url = self.url_prefix + "/v1/quota/lease"

        data = to_jsonable(body, expected=[V1GetTokenLeaseRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1GetTokenLeaseResponse])

    def quota_service_get_token(
        self, body: "V1GetTokenRequest"
    ) -> "V1GetTokenResponse":
        """
        Get a single token from Stanza Hub for access to given Guard (optional Feature name for priority).

        :param body: Requests token for given Guard at priority of specified feature.

        :return: OK
        """
        url = self.url_prefix + "/v1/quota/token"

        data = to_jsonable(body, expected=[V1GetTokenRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1GetTokenResponse])

    def quota_service_validate_token(
        self, body: "V1ValidateTokenRequest"
    ) -> "V1ValidateTokenResponse":
        """
        Validate quota access tokens with Stanza Hub.

        :param body: Calls Hub to validate a token (ensures token has not expired, was minted by Hub, and related to the specified Guard). Used from Ingress Guards. Ensures callers have acquired quota prior to expending resources.

        :return: OK
        """
        url = self.url_prefix + "/v1/quota/validatetokens"

        data = to_jsonable(body, expected=[V1ValidateTokenRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return from_obj(obj=resp.json(), expected=[V1ValidateTokenResponse])

    def stream_balancer_service_update_streams(
        self, body: "V1UpdateStreamsRequest"
    ) -> bytes:
        """
        Send a post request to /v1/updatestreams.

        :param body:

        :return:
        """
        url = self.url_prefix + "/v1/updatestreams"

        data = to_jsonable(body, expected=[V1UpdateStreamsRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content

    def usage_service_get_usage(self, body: "V1GetUsageRequest") -> bytes:
        """
        Send a post request to /v1/usage.

        :param body: Usage query.

        :return:
        """
        url = self.url_prefix + "/v1/usage"

        data = to_jsonable(body, expected=[V1GetUsageRequest])

        resp = self.session.request(
            method="post",
            url=url,
            json=data,
        )

        with contextlib.closing(resp):
            resp.raise_for_status()
            return resp.content


# Automatically generated file by swagger_to. DO NOT EDIT OR APPEND ANYTHING!
