# Locally Generated Python

This is the PR where we switched from using the buf.build hosted generated code to using this locally generated code: https://github.com/StanzaSystems/sdk-python/pull/35/files

We did this because we couldn't publish the `getstanza` to PyPi with this poetry supplemental source:

```toml
[[tool.poetry.source]]
name = "buf"
url = "https://buf.build/gen/python"
priority = "supplemental"
```

Ideally we would switch back to using the buf.build hosted generated python API code, but we need to figure out how to tell PyPi about the remote repository dependency.

Until such a time as we fix the above, pull new versions of the public APIs repo into the Stanza Python SDK by running:

```bash
buf generate https://github.com/StanzaSystems/apis.git
```