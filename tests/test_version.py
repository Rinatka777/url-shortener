from app.version import VERSION
import re

def test_version_non_empty():
    assert isinstance(VERSION, str)
    assert VERSION != ""

def test_version_format():
    assert re.match(r"^\d+\.\d+\.\d+$", VERSION)