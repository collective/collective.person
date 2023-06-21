<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/collective/collective.person/main/docs/logo.svg" width="100" /></div>

<h1 align="center">Person content type for Plone</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.person)](https://pypi.org/project/collective.person/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.person)](https://pypi.org/project/collective.person/)

[![Code analysis checks](https://github.com/collective/collective.person/actions/workflows/code-analysis.yml/badge.svg)](https://github.com/collective/collective.person/actions/workflows/code-analysis.yml)
[![Tests](https://github.com/collective/collective.person/actions/workflows/tests.yaml/badge.svg)](https://github.com/collective/collective.person/actions/workflows/tests.yml)
![Code Style](https://img.shields.io/badge/Code%20Style-Black-000000)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.person)](https://github.com/collective/collective.person)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.person?style=social)](https://github.com/collective/collective.person)

</div>

## Features

`collective.person` provides a content type representing a Person.

### Content Types

* `Person`: Represent a Person

### Permissions

| id | title | Usage |
| -- | -- | -- |
| collective.person.person.add | collective.person: Add Person | Control the creation of a new Person content item |

### Catalog Indexes

This package adds Indexes and Metadata to Portal Catalog.

| Content Attribute | Index Type | Metadata |
| -- | -- | -- |
| country | FieldIndex | ✅ |
| contact_email | FieldIndex | ❌ |

## See it in action

This package is being used by the following sites:

* TODO

## Documentation

### Installation

Add `collective.person` as a dependency on your package's `setup.py`

```python
    install_requires = [
        "collective.person",
        "Plone",
        "plone.restapi",
        "setuptools",
    ],
```

Also, add `collective.person` to your package's `configure.zcml` (or `dependencies.zcml`):

```xml
<include package="collective.person" />
```

### Generic Setup

To automatically enable this package when your add-on is installed, add the following line inside the package's `profiles/default/metadata.xml` `dependencies` element:

```xml
    <dependency>profile-collective.person:default</dependency>
```

## Source Code and Contributions

We welcome contributions to `collective.person`.

You can create an issue in the issue tracker, or contact a maintainer.

- [Issue Tracker](https://github.com/collective/collective.person/issues)
- [Source Code](https://github.com/collective/collective.person/)


### Development setup

You need a working Python environment version 3.8 or later.

Then install the dependencies and a development instance using:

```bash
make install
```

By default, we use the latest Plone version in the 6.x series.

### Update translations

```bash
make i18n
```
### Format codebase

```bash
make format
```
### Run tests

```bash
make test
```

## License

The project is licensed under GPLv2.
