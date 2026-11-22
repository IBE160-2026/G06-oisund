"""Fetch only the current Oslo day's public NVDB area as an import bundle."""

from datetime import datetime
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import ZIP_STORED, ZipFile

from .road_area_catalogue import BOX, MAX_ARCHIVE, OSLO
from .road_area_evidence import collect_area


def main():
    with TemporaryDirectory() as directory:
        path = Path(directory) / 'nvdb.zip'
        collect_area(datetime.now(OSLO).date(), BOX, path)
        if not 0 < path.stat().st_size <= MAX_ARCHIVE:
            raise ValueError('Daily NVDB archive exceeds its byte limit')
        with ZipFile(sys.stdout.buffer, 'w', compression=ZIP_STORED) as bundle:
            bundle.write(path, 'nvdb.zip')


if __name__ == '__main__':
    main()
