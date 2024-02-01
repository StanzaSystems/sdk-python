# Stanza Python SDK

Stanza is a developer-first tool for increasing reliability based on prioritized traffic management, quota allocation, and rate-limiting. On the back-end, it helps prevent downtime related to overload and excessive use of third-party APIs. On the front-end, it helps segment and weight your traffic, react automatically to overload or other conditions, and inspect the state of your critical user journeys.

"Stanza Python SDK" provides higher-order functions (["guards"](https://docs.dev.getstanza.dev/glossary#guard)) for adding this fault tolerance to your python 3.9+ application.

## Installation

The SDK is available on the Python Package Index (PyPI). You can install them via pip with the following command:

```shell
pip install getstanza
```
  
## Configuration

To use `sdk-python`, you'll need to import the `getstanza` package and initialize it with a [Stanza API Key](https://docs.dev.getstanza.dev/dashboard/administration/keys) and other options.

If not specified in the SDK initialization, the API Key, Service Name, Service Release, and Environment are read from the environment variables `STANZA_API_KEY`, `STANZA_SERVICE_NAME`, `STANZA_SERVICE_RELEASE`, and `STANZA_ENVIRONMENT`, respectively.

For more information, see the [Initialize Stanza section of our Python SDK documentation](https://docs.dev.getstanza.dev/gettingstarted/serversdk/python#initialize-stanza).

## Usage

The SDK supports weighted, prioritized, global rate limiting which is externally managed by the [Stanza Dashboard](https://docs.dev.getstanza.dev/dashboard).

The [samples/fastapi](./samples/fastapi) directory is a good place to start! (It's an example application which shows how to wrap inbound and outbound HTTP traffic with [Stanza Guards](https://docs.dev.getstanza.dev/configuration/guards).)

Or browse the [Official Stanza Documentation](https://docs.dev.getstanza.dev/) for more info on how to get started.

## Community

Join [Stanza's Community Discord](https://discord.gg/5feHXQam) to get involved and help us improve the SDK!