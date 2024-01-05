# sphinx-builder-classes

Exclude content blocks under particular Sphinx builders using classes.

## Installation

```bash
python -m pip install sphinx-builder-classes
```

To enable the extension in Sphinx, add the following to your conf.py:

```python
extension = ["sphinx-builder-classes"]
```

If you are using [ReadTheDocs](https://readthedocs.org/) to build your
documentation, the extension must be added as a requirement.

## Sphinx Configuration

In order to use this extension, you must define a set of class names to be
hidden by a given builder by setting `sphinx_builder_classes_builders`, e.g. in
your conf.py:

:::{code-block} python
:name: config-name

sphinx_builder_classes_builders = {
    "latex": ["no-latex"],
    "dirhtml": ["no-dirhtml"],
    "html": ["no-html"]
}
:::

For this example configuration ([](#config-name)), any element with the class
`"no-latex"` will be hidden for LaTeX builds, e.g.

```markdown
:::{note}
:class: no-latex

I won't appear in LaTeX output!
:::
```

You can also elect to hide an a set of classes for a particular output format,
instead of builder, by setting `sphinx_builder_classes_formats`, e.g. in your
conf.py:

:::{code-block} python
:name: config-format

sphinx_builder_classes_formats = {
    "latex": ["no-fmt-latex"],
    "html": ["no-fmt-html"]
}
:::

For this example configuration ([](#config-format)), any element with the class
`"no-fmt-html"` will be hidden for HTML-format builds, e.g.

```markdown
:::{note}
:class: no-fmt-html

I won't appear in any HTML-like outputs, e.g. dirhtml or html builders!
:::
```

## Example

The source code for this page contains two code blocks. Only one should be visible below!

:::{code-block} python
:class: no-html

print("Hello non-HTML builders")
:::

:::{code-block} python

print("Hello HTML and non-HTML builders")
:::
