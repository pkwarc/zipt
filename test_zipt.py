import zipfile
import pytest

import zipt
from zipt import (
    VERSION_FILENAME,
    UPDATED_FILENAME
)


TEST_FILE_CONTENT = 'Lorem ipsum dolor sit amet\nconsectetur adipiscing elit.\n'


@pytest.fixture
def tmp_dir(tmp_path):
    """
    Creates a directory with the following structure:
    /container/test0.txt
    /container/test1.txt
    /container/subcontainer/test3.txt
    """
    to_zip = tmp_path / 'container'
    txt0 = to_zip / 'text0.txt'
    txt0.parent.mkdir()
    txt0.touch()
    txt1 = to_zip / 'text1.txt'
    txt1.touch()
    sub_to_zip = to_zip / 'subcontainer'
    sub_to_zip.mkdir()
    txt3 = sub_to_zip / 'text3.txt'
    for test_file in (txt0, txt1, txt3):
        with open(test_file, mode='wb') as f:
            f.write(TEST_FILE_CONTENT.encode('utf-8'))
    return to_zip


def assert_tmp_dir(zip_path, version=None, updated=None):
    def assert_file_exists(name, content):
        file_zip_path = zipfile.Path(zip_path, name)
        assert file_zip_path.exists()
        assert file_zip_path.read_text() == content
    if version:
        assert_file_exists(VERSION_FILENAME, version)
    if updated:
        assert_file_exists(UPDATED_FILENAME, updated)
    # compare with the dir structure created by tmp_dir fixture
    assert_file_exists('container/text0.txt', TEST_FILE_CONTENT)
    assert_file_exists('container/text1.txt', TEST_FILE_CONTENT)
    assert_file_exists('container/subcontainer/text3.txt', TEST_FILE_CONTENT)


def test_create_zip_from_dir(tmp_dir):
    version = 'v0.1.0'
    overwrites = {
        VERSION_FILENAME: version
    }
    zip_path = zipt.create_zip(tmp_dir, overwrites)

    assert_tmp_dir(zip_path, version)


def test_update_zip_version(tmp_dir):
    initial = 'v0.1.0'
    want = 'v0.2.0'
    overwrites = {
        VERSION_FILENAME: initial
    }
    zip_path = zipt.create_zip(tmp_dir, overwrites)

    overwrites[VERSION_FILENAME] = want
    zipt.update_zip(zip_path, overwrites)

    assert_tmp_dir(zip_path, version=want)


def test_create_zip_from_dir_add_updated_txt_file(tmp_dir):
    version = 'v0.1.0'
    updated_at = '2021-02-05'
    overwrites = {
        VERSION_FILENAME: version,
        UPDATED_FILENAME: updated_at
    }

    zip_path = zipt.create_zip(tmp_dir, overwrites)

    assert_tmp_dir(zip_path, version=version, updated=updated_at)


def test_update_zip_add_updated_txt_file(tmp_dir):
    version = 'v0.1.0'
    updated_at = '2021-02-05'
    overwrites = {
        VERSION_FILENAME: version,
    }
    zip_path = zipt.create_zip(tmp_dir, overwrites)

    overwrites[UPDATED_FILENAME] = updated_at
    zipt.update_zip(zip_path, overwrites)

    assert_tmp_dir(zip_path, version=version, updated=updated_at)
