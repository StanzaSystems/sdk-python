import datetime
import os
import uuid
from typing import Optional

CONFIG_POLL_INTERVAL_SECS = 15


class StanzaConfiguration:
    """

    The StanzaConfiguration class represents the configuration for the Stanza service. It allows setting various properties such as the API key, service name, service release, environment, and hub address.

    Constructor:
        def __init__(self, api_key: Optional[str], service_name: Optional[str],
                     service_release: Optional[str], environment: Optional[str],
                     hub_address: Optional[str])

            Initializes a new instance of the StanzaConfiguration class.

            Parameters:
                - api_key (Optional[str]): The API key to authenticate with the Stanza service. If not provided, it will attempt to read from the "STANZA_API_KEY" environment variable.
                - service_name (Optional[str]): The name of the service. If not provided, it will attempt to read from the "STANZA_SERVICE_NAME" environment variable.
                - service_release (Optional[str]): The release version of the service. If not provided, it defaults to "0.0.0".
                - environment (Optional[str]): The environment name of the service. If not provided, it defaults to "dev".
                - hub_address (Optional[str]): The address of the Stanza hub. If not provided, it defaults to "hub.stanzasys.co:9020".

    Properties:
        - api_key (str): Returns the API key used for authentication.
        - service_name (str): Returns the name of the service.
        - service_release (str): Returns the release version of the service.
        - environment (str): Returns the environment name of the service.
        - hub_address (str): Returns the address of the Stanza hub.
        - interval (timedelta): Returns the interval between configuration polls.
        - client_id (str): Returns the unique client ID generated for this configuration.
        - customer_id (Optional[str]): Returns the customer ID associated with this configuration.
        - metadata (List[Tuple[str, str]]): Returns the metadata associated with this configuration.

    Methods:
        - _get_setting(input_value: Optional[str], env_var_name: str, default: Optional[str] = None,
                       require_value: bool = False) -> Optional[str]

            This is a private helper method used to get the setting value based on the input value, environment variable, default value, and whether a value is required or not. It returns the setting value based on the following rules:
                - If the input_value is not None, it returns the input_value.
                - If the env_var_name environment variable is set, it returns its value.
                - If require_value is True and no value is found, it raises a ValueError indicating the missing required environment variable.
                - Otherwise, it returns the default value.

    """

    def __init__(self, api_key: Optional[str], service_name: Optional[str],
                 service_release: Optional[str], environment: Optional[str],
                 hub_address: Optional[str]):
        """
        Initialize a new instance of the class.

        :param api_key: An optional string representing the API key.
        :param service_name: An optional string representing the service name.
        :param service_release: An optional string representing the service release version.
        :param environment: An optional string representing the environment.
        :param hub_address: An optional string representing the hub address.

        :return: None
        """
        self.api_key = self._get_setting(api_key, "STANZA_API_KEY", None, True)
        self.service_name = self._get_setting(service_name, "STANZA_SERVICE_NAME", None, True)
        self.service_release = self._get_setting(service_release, "STANZA_SERVICE_RELEASE", "0.0.0")
        self.environment = self._get_setting(environment, "STANZA_ENVIRONMENT", "dev")
        self.hub_address = self._get_setting(hub_address, "STANZA_HUB_ADDRESS", "hub.stanzasys.co:9020")
        self.interval = datetime.timedelta(seconds=CONFIG_POLL_INTERVAL_SECS)
        self.client_id = str(uuid.uuid4())
        self.customer_id: Optional[str] = None
        self.metadata = [("x-stanza-key", self.api_key)]

    @staticmethod
    def _get_setting(input_value: Optional[str], env_var_name: str, default: Optional[str] = None,
                     require_value: bool = False) -> Optional[str]:
        """
            _get_setting(input_value: Optional[str], env_var_name: str, default: Optional[str] = None,
                         require_value: bool = False) -> Optional[str]

            Retrieves a setting value based on the given input value, environment variable, default value, and requirement flag.

            Parameters:
                input_value (Optional[str]): The input value to be checked. If a non-null value is provided, it is returned as the setting value.
                env_var_name (str): The name of the environment variable. If it is set, the value of the environment variable is returned as the setting value.
                default (Optional[str], optional): The default value to be returned if no other value is found. Defaults to None.
                require_value (bool, optional): Specifies whether the setting value is required. If set to True and no value is found, a ValueError is raised. Defaults to False.

            Returns:
                Optional[str]: The retrieved setting value or None if no value is found and no default is specified.

            Raises:
                ValueError: If require_value is True and no value is found.

            Example Usage:
                input_value = "example"
                env_var_name = "MY_SETTING"
                default = "default_value"
                require_value = False

                result = _get_setting(input_value, env_var_name, default=default, require_value=require_value)

                print(result)  # "example"
        """
        if input_value is not None:
            return input_value

        env_value = os.environ.get(env_var_name)
        if env_value is not None:
            return env_value

        if require_value:
            raise ValueError(f"Missing required {env_var_name.replace('_', ' ').title()} "
                             f"(Hint: Set a {env_var_name} environment variable!)")

        return default
