# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2023 Anna <cyber@sysrq.in>
# No warranty

from copy import deepcopy
from pathlib import Path

import pytest

from gentle.generators.python.wheel import WheelGenerator
from gentle.metadata import MetadataXML

from tests.utils import compare_mxml


def test_pkg_none(mxml: MetadataXML):
    gen = WheelGenerator(Path(__file__).parent / "pkg_none")
    assert not gen.active


@pytest.mark.net
@pytest.mark.parametrize("dirname", ["pyproject.toml", "setup.cfg", "setup.py"])
def test_pkg_empty(mxml: MetadataXML, dirname: str):
    gen = WheelGenerator(Path(__file__).parent / "pkg_empty" / dirname)
    assert gen.active

    mxml_old = deepcopy(mxml)
    gen.update_metadata_xml(mxml)
    assert compare_mxml(mxml_old, mxml) == ""
