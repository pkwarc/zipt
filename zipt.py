#! /usr/bin/env python

import argparse
import pathlib
import sys
import tempfile
import zipfile
import os
import logging

from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime as DateTime


VERSION_FILENAME = 'VERSION.txt'
UPDATED_FILENAME = 'updated.txt'
_logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Create a compressed zip file and specify its version')
    parser.add_argument(
        'zip',
        help='The zip file which version is to be updated, or a file to create the zip from',
        type=pathlib.Path
    )
    parser.add_argument(
        'version',
        help=f'A version to be put in a "{VERSION_FILENAME}" file inside the zip'
    )
    parser.add_argument(
        '-u',
        '--updated',
        help=f'Insert into the zip a file "{UPDATED_FILENAME}" with the current UTC time',
        action='store_true'
    )
    args = parser.parse_args()
    overwrites = {
        VERSION_FILENAME: f'{args.version}\n',
    }

    if not args.zip.exists():
        sys.exit(f'File "{args.zip}" does not exist')
    if args.updated:
        now = DateTime.utcnow()
        overwrites[UPDATED_FILENAME] = now.strftime('%Y%m%d %H%M%S')
    if not zipfile.is_zipfile(args.zip):
        create_zip(args.zip, overwrites)
    else:
        update_zip(args.zip, overwrites)


def update_zip(src_zip: pathlib.Path, overwrites: dir):
    src_path = pathlib.Path(src_zip)
    tmpfd, tmpname = tempfile.mkstemp(dir=src_path.parent)
    os.close(tmpfd)

    with ZipFile(src_zip) as src, ZipFile(tmpname, 'w') as dst:
        for zipinfo in src.infolist():
            if zipinfo.filename in overwrites.keys():
                continue
            dst.writestr(zipinfo, src.read(zipinfo))

    os.remove(src_zip)
    os.rename(tmpname, src_zip)

    with ZipFile(src_zip, 'a', ZIP_DEFLATED) as dst:
        for filename, content in overwrites.items():
            dst.writestr(filename, content)
    return src_path


def create_zip(src: pathlib.Path, overwrites: dict):
    path = src.expanduser().resolve(strict=True)
    zip_path = f'{path}.zip'

    with ZipFile(zip_path, 'w', ZIP_DEFLATED) as dst:
        for file in path.rglob('*'):
            if file.name not in overwrites.keys():
                dst.write(file, file.relative_to(path.parent))
        for filename, content in overwrites.items():
            dst.writestr(filename, content)
    return zip_path


if __name__ == '__main__':
    main()
