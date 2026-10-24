"""Readable source uncertainties, without guessing missing facts."""

def issue_text(issue):
    field = {'start': 'start', 'end': 'slutt'}.get(issue.get('field'), 'tidspunkt')
    names = {
        'unresolved_time': f'Kontroller {field}: klokkeslett eller kalenderdato er ukjent.',
        'missing_endpoint': 'Endested mangler i tolkningen. Kontroller mot kilden.',
        'unrecognized_source_line': 'En kilderad kunne ikke tolkes. Kontroller kilden.',
        'unproven_calendar_interval': 'Kalenderdatoene kunne ikke fastslås fra skiftintervallet.',
        'reversed_activity_time': 'Slutt ligger før start. Kontroller dato og klokkeslett.',
    }
    return names.get(issue['code'], f'Ukjent kildeusikkerhet ({issue["code"]}).')


def annotation_rows(source):
    """Attach unknown markers to the nearest preceding source activity on that column."""
    result = {}
    for annotation in source['annotations']:
        location = annotation['provenance']
        if location.get('line') is None or location.get('column') is None:
            continue
        candidates = []
        for row in source['activities']:
            for locations in row['provenance'].values():
                if not isinstance(locations, list):
                    continue
                for point in locations:
                    if point.get('line') is not None and (point.get('page'), point.get('column')) == (location.get('page'), location.get('column')) and point['line'] <= location['line']:
                        candidates.append((point['line'], row['source_order']))
        if candidates:
            result.setdefault(max(candidates)[1], []).append(annotation)
    return result


def marker_fragments(content):
    """Known document fragments are neutral independently of row association."""
    return list(dict.fromkeys(
        f'Kildemerket {marker.value} har ukjent betydning (side {marker.provenance.page}).'
        for marker in content.import_metadata.annotations
    )) if content.import_metadata else []


def current_uncertainty(content, activity, fragments=None):
    """Hide only exact old generated marker fragments, retaining stored text."""
    value = activity.uncertainty or ''
    for fragment in marker_fragments(content) if fragments is None else fragments:
        value = value.replace(fragment, '')
    return value.strip()
