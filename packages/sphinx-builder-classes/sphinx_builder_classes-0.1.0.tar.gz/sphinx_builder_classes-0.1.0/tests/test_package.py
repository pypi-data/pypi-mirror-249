from __future__ import annotations

import importlib.metadata

import sphinx_builder_classes as m


def test_version():
    assert importlib.metadata.version("sphinx_builder_classes") == m.__version__
