from getstanza import hub


class New:
    """Initialize new Stanza state."""

    def __init__(
        self,
        api_key: str,
        service_name: str,
        service_release: str,
        environment: str,
        hub_address: str,
    ) -> None:
        self.api_key = api_key
        self.service_name = service_name
        self.release = service_release
        self.environment = environment
        self.hub_address = hub_address

        # TODO: we need a robust hub connection and poller (for getting service, guard, etc)
        #       configs -- below is just a SIMPLE proof-of-concept for seeing that the
        #       swagger_to produce hub package is working
        hub_conn = hub.RemoteCaller(
            url_prefix=hub_address, headers={"X-Stanza-Key": api_key}
        )
        token = hub_conn.auth_service_get_bearer_token(environment=environment)
        print(token)
