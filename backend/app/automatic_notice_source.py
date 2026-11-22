"""Normalize bounded public SIRI-SX observations without retaining the raw XML."""

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import urlsplit
from xml.etree.ElementTree import TreeBuilder
from xml.parsers import expat

from pydantic import AnyHttpUrl, TypeAdapter


SIRI = '{http://www.siri.org.uk/siri}'
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
PAGE_SIZE = 5
# These limits apply before persistence. Expat dials no external resources;
# the parser also rejects all DTDs, including internal entity declarations.
MAX_XML_BYTES = 512 * 1024
MAX_XML_DEPTH = 32
MAX_XML_NODES = 5_000
MAX_TEXT = 16_384
MAX_ID = 200
SITUATION_PREFIX = 'TRO:SituationNumber:'
MAX_NORMALIZED_ITEM_BYTES = 64 * 1024
HTTP_URL = TypeAdapter(AnyHttpUrl)


class SourceError(ValueError):
    def __init__(self, code, retry_after=0):
        super().__init__(code)
        self.code = code
        self.retry_after = retry_after


@dataclass(frozen=True)
class Page:
    response_at: datetime
    more: bool
    items: list[dict]


def xml_tree(value):
    if not value or len(value) > MAX_XML_BYTES:
        raise SourceError('xml-size')
    parser = expat.ParserCreate(namespace_separator='}')
    builder = TreeBuilder()
    depth = nodes = 0

    def expanded(name):
        return '{' + name if '}' in name else name

    def start(name, attrs):
        nonlocal depth, nodes
        depth += 1
        nodes += 1
        if depth > MAX_XML_DEPTH or nodes > MAX_XML_NODES:
            raise SourceError('xml-complexity')
        builder.start(expanded(name), {expanded(key): val for key, val in attrs.items()})

    def end(name):
        nonlocal depth
        builder.end(expanded(name))
        depth -= 1

    def forbid(*_):
        raise SourceError('xml-doctype')

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = builder.data
    parser.StartDoctypeDeclHandler = forbid
    parser.ExternalEntityRefHandler = forbid
    try:
        parser.Parse(value, True)
        return builder.close()
    except (expat.ExpatError, LookupError, ValueError) as error:
        if isinstance(error, SourceError):
            raise
        raise SourceError('xml-invalid') from None


def field(parent, name, required=False):
    matches = parent.findall(SIRI + name)
    if len(matches) > 1 or (required and not matches):
        raise SourceError('field-' + name)
    return matches[0] if matches else None


def scalar(parent, name, required=False, limit=MAX_ID):
    node = field(parent, name, required)
    if node is None:
        return None
    value = (node.text or '').strip()
    if len(node) or len(value) > limit or (required and not value):
        raise SourceError('field-' + name)
    return value or None


def instant(value):
    if not isinstance(value, str) or value.endswith('-00:00') or not re.fullmatch(
        r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d{1,12})?)?(Z|[+-]\d{2}:\d{2})', value
    ):
        return None
    try:
        return datetime.fromisoformat(value).astimezone(UTC)
    except (ValueError, OverflowError):
        return None


def safe_link(value):
    if not value or '\\' in value or any(ord(ch) <= 32 or ord(ch) == 127 for ch in value):
        return None
    try:
        parts = urlsplit(value)
        if parts.scheme in {'http', 'https'} and parts.hostname and not parts.username and not parts.password:
            HTTP_URL.validate_python(value)
            return value
    except ValueError:
        pass
    return None


def localized(node, name):
    values = []
    for item in node.findall(SIRI + name):
        if len(item) or len(item.text or '') > MAX_TEXT:
            raise SourceError('field-' + name)
        values.append({'text': item.text or '', 'language': item.get(XML_LANG)})
    return values


def selector(node):
    # Store simple typed facts and their nesting, without copying XML markup.
    value = (node.text or '').strip() or None
    if value and len(value) > MAX_TEXT:
        raise SourceError('selector-size')
    return {'kind': node.tag.removeprefix(SIRI), 'value': value,
            'children': [selector(child) for child in node]}


def valid_situation(value):
    return (isinstance(value, str) and value.startswith(SITUATION_PREFIX)
            and len(SITUATION_PREFIX) < len(value) <= MAX_ID
            and not any(char == '\0' or 0xD800 <= ord(char) <= 0xDFFF for char in value))


def normalize(node):
    participant = scalar(node, 'ParticipantRef', required=True)
    situation = scalar(node, 'SituationNumber', required=True)
    if participant != 'TRO' or not valid_situation(situation):
        raise SourceError('source-scope')
    affects = field(node, 'Affects')
    links = field(node, 'InfoLinks')
    return {
        'participant': participant, 'situation': situation,
        'version': scalar(node, 'Version'), 'publisher_updated_at': scalar(node, 'VersionedAtTime'),
        'source_created_at': scalar(node, 'CreationTime'), 'progress': scalar(node, 'Progress'),
        'source_type': scalar(node, 'SourceType'), 'severity': scalar(node, 'Severity'),
        'report_type': scalar(node, 'ReportType'),
        'summary': localized(node, 'Summary'), 'description': localized(node, 'Description'),
        'advice': localized(node, 'Advice'),
        'links': [] if links is None else [url for item in links.findall(SIRI + 'InfoLink')
                                         if (url := safe_link(scalar(item, 'Uri', limit=2_048)))],
        'windows': [{'start': scalar(period, 'StartTime'), 'end': scalar(period, 'EndTime')}
                    for period in node.findall(SIRI + 'ValidityPeriod')],
        'affects': [] if affects is None else [selector(child) for child in affects],
        'verified_siri_scope': affects is not None and all(
            element.tag.startswith(SIRI) and not element.attrib for element in affects.iter()
        ),
    }


def revision(content):
    return hashlib.sha256(canonical(content)).hexdigest()


def source_revision(content):
    # Namespace verification belongs to the local observation. Keep the revision
    # of the publisher's normalized facts stable when that proof is refreshed.
    return revision({key: value for key, value in content.items() if key != 'verified_siri_scope'})


def canonical(content):
    return json.dumps(content, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def parse_page(value, headers, requestor):
    if headers.get('datasetid') != 'TRO' or headers.get('requestorid') != str(requestor):
        raise SourceError('header-continuity')
    root = xml_tree(value)
    if root.tag != SIRI + 'Siri' or root.get('version') not in (None, '2.0'):
        raise SourceError('siri-envelope')
    service = field(root, 'ServiceDelivery', required=True)
    delivery = field(service, 'SituationExchangeDelivery', required=True)
    for level in (service, delivery):
        if scalar(level, 'Status') not in (None, 'true') or field(level, 'ErrorCondition') is not None:
            raise SourceError('delivery-status')
    levels = (service, delivery)
    echoes = [scalar(level, 'RequestMessageRef', required=True) for level in levels
              if field(level, 'RequestMessageRef') is not None]
    if echoes != [str(requestor)]:
        raise SourceError('xml-continuity')
    flags = [scalar(level, 'MoreData', required=True) for level in levels if field(level, 'MoreData') is not None]
    flags.extend(level.attrib['MoreData'] for level in levels if 'MoreData' in level.attrib)
    if flags not in (['true'], ['false']):
        raise SourceError('more-data')
    response_at = instant(scalar(delivery, 'ResponseTimestamp') or scalar(service, 'ResponseTimestamp', required=True))
    if response_at is None:
        raise SourceError('response-time')
    situations = field(delivery, 'Situations', required=True)
    if len(situations) > PAGE_SIZE or any(node.tag != SIRI + 'PtSituationElement' for node in situations):
        raise SourceError('situation-collection')
    items = [normalize(node) for node in situations]
    if any(len(canonical(item)) > MAX_NORMALIZED_ITEM_BYTES for item in items):
        raise SourceError('normalized-item-size')
    return Page(response_at, flags == ['true'], items)
