# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

from pathlib import Path

import pytest

from gentle.metadata import MetadataXML
from gentle.pms.portagepm import parse_mxml


def pytest_addoption(parser):
    parser.addoption("--net", action="store_true",
                     help="run tests that connect to network")
    parser.addoption("--with-perl", action="store_true",
                     help="run tests that require Perl")


def pytest_configure(config):
    config.addinivalue_line("markers", "net: mark test as using network")
    config.addinivalue_line("markers", "perl: mark test as using Perl")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--net"):
        skip_net = pytest.mark.skip(reason="need --net option to run")
        for item in items:
            if "net" in item.keywords:
                item.add_marker(skip_net)

    if not config.getoption("--with-perl"):
        skip_perl = pytest.mark.skip(reason="need --with-perl option to run")
        for item in items:
            if "perl" in item.keywords:
                item.add_marker(skip_perl)


@pytest.fixture
def mxml() -> MetadataXML:
    return MetadataXML(Path(__file__).parent / "metadata.xml", parse_mxml)
