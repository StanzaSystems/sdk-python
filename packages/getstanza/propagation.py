"""Constants and utility functions that assist with propagation."""

from contextvars import ContextVar
from typing import Mapping, Optional

from opentelemetry import baggage
from opentelemetry.context import Context as OTELContext
from opentelemetry.propagate import get_global_textmap

STZ_BOOST = "stz-boost"
STZ_FEAT = "stz-feat"

OTEL_CONTEXT_KEY = "stanza-context"
OUTBOUND_HEADERS_KEY = "stanza-outbound-headers"

UBERCTX_STZ_BOOST_KEY = f"uberctx-{STZ_BOOST}"
UBERCTX_STZ_FEAT_KEY = f"uberctx-{STZ_FEAT}"
OT_STZ_BOOST_KEY = f"ot-baggage-{STZ_BOOST}"
OT_STZ_FEAT_KEY = f"ot-baggage-{STZ_FEAT}"

STANZA_INBOUND_HEADERS = [
    UBERCTX_STZ_BOOST_KEY,
    UBERCTX_STZ_FEAT_KEY,
    OT_STZ_BOOST_KEY,
    OT_STZ_FEAT_KEY,
]

# We bind request and baggage to the request context using contextvars.
StanzaContext: ContextVar[OTELContext] = ContextVar(OTEL_CONTEXT_KEY)
StanzaOutgoingHeaders: ContextVar[dict[str, str]] = ContextVar(OUTBOUND_HEADERS_KEY)


def context_from_http_headers(headers: Mapping[str, str]) -> OTELContext:
    """
    Creates a new context with baggage from the baggage header, in addition to
    baggage contained in extra headers used by Jaeger and Datadog.
    """

    def lowercase_pair_key(pair):
        key, value = pair.split("=")

        return f"{key.lower()}={value}"

    otel_baggage = [
        lowercase_pair_key(pair)
        for pair in filter(lambda pair: pair, headers.get("baggage", "").split(","))
    ]

    for inbound_header in STANZA_INBOUND_HEADERS:
        if inbound_header in headers:
            otel_baggage.append(f"{inbound_header}={headers[inbound_header]}")

    carrier = {"baggage": ",".join(otel_baggage)}

    context = get_global_textmap().extract(carrier)
    StanzaContext.set(context)

    return context


def http_headers_from_context() -> dict[str, str]:
    """Returns HTTP headers corresponding to baggage in the current context."""

    headers: dict[str, str] = {}
    baggage_pairs: dict[str, str] = {}

    # Add Jaeger and Datadog baggage separately since they should be passed
    # with their own headers rather than with the main baggage header.
    for key, value in StanzaOutgoingHeaders.get().items():
        headers[key] = value

    # Collect baggage pairs that don't have their own unique headers.
    for key, value in baggage.get_all(StanzaContext.get()).items():
        if key not in STANZA_INBOUND_HEADERS:
            baggage_pairs[key.lower()] = str(value)

    # Add 'baggage' with all pairs that aren't in 'STANZA_INBOUND_HEADERS'.
    headers["baggage"] = ",".join(
        map(lambda pair: f"{pair[0]}={pair[1]}", baggage_pairs.items())
    )

    return headers


def get_feature(feature: Optional[str] = None) -> Optional[str]:
    """Return the feature from baggage, or the one provided."""

    _feature: Optional[str] = None
    context = StanzaContext.get()

    if feature is not None:
        _feature = feature
    elif baggage_feat := (
        baggage.get_baggage(STZ_FEAT, context)
        or baggage.get_baggage(UBERCTX_STZ_FEAT_KEY, context)
        or baggage.get_baggage(OT_STZ_FEAT_KEY, context)
    ):
        _feature = str(baggage_feat)

    if not baggage.get_baggage(STZ_FEAT, context) and _feature is not None:
        context = baggage.set_baggage(STZ_FEAT, _feature, context)
        StanzaContext.set(context)

    # Update outgoing headers with additional headers for Jaeger and Datadog.
    if _feature is not None:
        outgoing_headers = StanzaOutgoingHeaders.get({})
        outgoing_headers[UBERCTX_STZ_FEAT_KEY] = _feature
        outgoing_headers[OT_STZ_FEAT_KEY] = _feature
        StanzaOutgoingHeaders.set(outgoing_headers)

    return _feature


def get_priority_boost(priority_boost: Optional[int] = None) -> Optional[int]:
    """Return the priority boost from baggage, or the one provided."""

    _priority_boost: Optional[int] = None
    context = StanzaContext.get()

    if priority_boost is not None:
        _priority_boost = priority_boost

    if baggage_boost := (
        baggage.get_baggage(STZ_BOOST, context)
        or baggage.get_baggage(UBERCTX_STZ_BOOST_KEY, context)
        or baggage.get_baggage(OT_STZ_BOOST_KEY, context)
    ):
        _priority_boost = (
            (_priority_boost or 0) + int(baggage_boost)
            if isinstance(baggage_boost, (str, int))
            else None
        )

    if not baggage.get_baggage(STZ_BOOST, context) and _priority_boost is not None:
        baggage.set_baggage(STZ_BOOST, _priority_boost, context)

    # Update outgoing headers with additional headers for Jaeger and Datadog.
    if _priority_boost is not None:
        outgoing_headers = StanzaOutgoingHeaders.get({})
        outgoing_headers[UBERCTX_STZ_BOOST_KEY] = str(_priority_boost)
        outgoing_headers[OT_STZ_BOOST_KEY] = str(_priority_boost)
        StanzaOutgoingHeaders.set(outgoing_headers)

    return _priority_boost
