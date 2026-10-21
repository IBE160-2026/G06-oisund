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
        candidates = []
        for row in source['activities']:
            for locations in row['provenance'].values():
                if not isinstance(locations, list):
                    continue
                for point in locations:
                    if (point.get('page'), point.get('column')) == (location.get('page'), location.get('column')) and point.get('line', 0) <= location.get('line', 0):
                        candidates.append((point.get('line', 0), row['source_order']))
        if candidates:
            result.setdefault(max(candidates)[1], []).append(annotation)
    return result
