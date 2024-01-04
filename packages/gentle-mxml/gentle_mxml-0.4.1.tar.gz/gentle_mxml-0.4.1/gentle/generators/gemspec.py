# SPDX-License-Identifier: WTFPL
# SPDX-FileCopyrightText: 2022 Anna <cyber@sysrq.in>
# No warranty

"""
Metadata XML generator for Crystal Shards.

The following attributes are supported:

* Upstream maintainer(s)
* Upstream documentation
* Remote ID
"""

import logging
from pathlib import Path

from gentle.generators import AbstractGenerator
from gentle.metadata import MetadataXML
from gentle.metadata.utils import extract_remote_id

try:
    import yaml
    from yaml import Loader
    _HAS_PYYAML = True

    class VersionTag(yaml.YAMLObject):
        """ Dummy version tag """
        yaml_tag = "!ruby/object:Gem::Version"

    class RequirementTag(yaml.YAMLObject):
        """ Dummy requirement tag """
        yaml_tag = "!ruby/object:Gem::Requirement"

    class DependencyTag(yaml.YAMLObject):
        """ Dummy dependency tag """
        yaml_tag = "!ruby/object:Gem::Dependency"

    class SpecificationTag(yaml.YAMLObject):
        """ Dummy specification tag """
        yaml_tag = "!ruby/object:Gem::Specification"
except ModuleNotFoundError:
    _HAS_PYYAML = False

logger = logging.getLogger("gemspec")


class GemspecGenerator(AbstractGenerator):
    def __init__(self, srcdir: Path):
        self.metadata_yml = srcdir / "all" / "metadata"

    def update_metadata_xml(self, mxml: MetadataXML) -> None:
        with open(self.metadata_yml) as file:
            if (metadata := yaml.load(file, Loader)) is None:
                return

        if metadata.homepage:
            logger.info("Found homepage: %s", metadata.homepage)
            if (remote_id := extract_remote_id(metadata.homepage)) is not None:
                mxml.add_upstream_remote_id(remote_id)

        for name, value in metadata.metadata.items():
            if not isinstance(value, str):
                continue

            logger.info("Found %s: %s", name, value)
            match name:
                case "bug_tracker_uri":
                    mxml.set_upstream_bugs_to(value)
                case "changelog_uri":
                    mxml.set_upstream_changelog(value)
                case "documentation_uri":
                    mxml.set_upstream_doc(value)
                case "homepage_uri" | "source_code_uri":
                    if (remote_id := extract_remote_id(value)) is not None:
                        mxml.add_upstream_remote_id(remote_id)

    @property
    def active(self) -> bool:
        return _HAS_PYYAML and self.metadata_yml.is_file()
