"""
Copyright (c) 2024 Angus Hollands. All rights reserved.

sphinx-builder-classes: Sphinx extension to hide content based upon the active builder
"""


from __future__ import annotations

from typing import Any

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx.util.docutils import SphinxTranslator

from ._version import version as __version__

__all__ = ["__version__"]


class HiddenNode(nodes.Element):
    """A node that will not be rendered."""

    @classmethod
    def register(cls, app: Sphinx) -> None:
        """Register a special `HiddenNode` element that does not produce any rendered output."""
        app.add_node(
            cls,
            override=True,
            html=(visit_HiddenNode, None),
            latex=(visit_HiddenNode, None),
            textinfo=(visit_HiddenNode, None),
            text=(visit_HiddenNode, None),
            man=(visit_HiddenNode, None),
        )


def visit_HiddenNode(self: SphinxTranslator, node: nodes.Element) -> None:  # noqa: ARG001, pylint: disable=invalid-name
    """No-op visitor for the special `HiddenNode` element."""
    raise nodes.SkipNode


class HideNodesTransform(SphinxPostTransform):
    """Hides nodes with the given classes during rendering."""

    default_priority = 400

    def run(self, **kwargs: Any) -> None:  # noqa: ARG002
        """Replace nodes tagged with builder-specific classes with a special `HiddenNode`."""
        builder_ignore_classes = self.app.config["sphinx_builder_classes_builders"]
        ignore_classes = set(builder_ignore_classes.get(self.app.builder.name, set()))

        format_ignore_classes = self.app.config["sphinx_builder_classes_formats"]
        ignore_classes |= set(format_ignore_classes.get(self.app.builder.format, set()))

        for node in self.document.traverse(nodes.Element):
            node_classes = set(node["classes"])
            if node_classes & ignore_classes:
                node.replace_self([HiddenNode()])


DEFAULT_BUILDER_IGNORE_CLASSES = {
    "latex": [
        "dropdown",
        "toggle",
        "margin",
    ]
}

DEFAULT_FORMAT_IGNORE_CLASSES = {
    "latex": [
        "dropdown",
        "toggle",
        "margin",
    ]
}


def setup(app: Sphinx) -> None:
    """Setup Sphinx extension."""
    app.connect("builder-inited", setup_transforms)
    app.add_config_value(
        "sphinx_builder_classes_builders", DEFAULT_BUILDER_IGNORE_CLASSES, "env", [dict]
    )
    app.add_config_value(
        "sphinx_builder_classes_formats", DEFAULT_FORMAT_IGNORE_CLASSES, "env", [dict]
    )


def setup_transforms(app: Sphinx) -> None:  # pylint: disable=unused-argument
    """Setup custom Sphinx transformations, and register custom nodes."""
    app.add_post_transform(HideNodesTransform)
    HiddenNode.register(app)
