<div align="center"><img alt="logo" src="https://raw.githubusercontent.com/collective/collective.person/main/docs/logo.svg" width="100" /></div>

<h1 align="center">Person content type for Plone</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - License](https://img.shields.io/pypi/l/collective.person)](https://pypi.org/project/collective.person/)
[![PyPI - Status](https://img.shields.io/pypi/status/collective.person)](https://pypi.org/project/collective.person/)


[![PyPI - Plone Versions](https://img.shields.io/pypi/frameworkversions/plone/collective.person)](https://pypi.org/project/collective.person/)

[![CI](https://github.com/collective/collective.person/actions/workflows/ci.yml/badge.svg)](https://github.com/collective/collective.person/actions/workflows/ci.yml)

[![GitHub contributors](https://img.shields.io/github/contributors/collective/collective.person)](https://github.com/collective/collective.person)
[![GitHub Repo stars](https://img.shields.io/github/stars/collective/collective.person?style=social)](https://github.com/collective/collective.person)

</div>

## Features

`collective.person` provides a content type representing a Person.

### Content Types

* `Person`: A content type representing a person

### Behaviors

| name | title | description |
| -- | -- | -- |
| `collective.person.person` | Person Behavior | Fields with basic person information |
| `collective.person.user` | Link Person to Plone User | Adapts a Person to link it to a Plone User |
| `collective.person.namefromusername` | Name from username |Use the username field as name (basis for the id) |

### Permissions

| id | title | Usage |
| -- | -- | -- |
| collective.person.person.add | collective.person: Add Person | Control the creation of a new Person content item |

### Catalog Indexes

This package adds Indexes and Metadata to Portal Catalog.

| Content Attribute | Index Type | Metadata | Comment |
| -- | -- | -- | -- |
| roles | KeywordIndex | ✅ | -- |
| username | FieldIndex | ✅ | Used when `collective.person.user` behavior is enabled |

## See it in action

This package is being used by the following sites:

* TODO

## Documentation

### Installation

Add `collective.person` as a dependency on your package's `setup.py`

```python
    install_requires = [
        "Plone",
        "plone.restapi",
        "collective.person",
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
### Lint codebase

```bash
make lint
```
### Run tests

```bash
make test
```

## Extending collective.person

### Customizing how the title is generated

`collective.person` provides two built-in strategies for generating the title of a **Person** object:

- **First and Last Name** (`first_last`):
  The title is generated using the template `{first_name} {last_name}`.
  Example: `first_name="Douglas"`, `last_name="Adams"` → **Douglas Adams**

- **Last and First Name** (`last_first`):
  The title is generated using the template `{last_name}, {first_name}`.
  Example: `first_name="Douglas"`, `last_name="Adams"` → **Adams, Douglas**

You can select the preferred option in the **Person control panel**.


### Providing your own title generator

If the default options do not fit your needs, you can register a custom utility that implements the `collective.person.interfaces.IPersonTitle` interface.

#### Step 1: Create your generator

For example, create a file called `title_generator.py` in your package:

```python
from collective.person.content.person import Person
from collective.person.interfaces import IPersonTitle
from zope.interface import implementer


@implementer(IPersonTitle)
class MyTitleGenerator:
    """Return the title with a custom prefix."""

    name: str = "My title generator"

    def title(self, context: Person) -> str:
        """Return the title of the person."""
        first_name = context.first_name
        last_name = context.last_name or ""
        return f"Human {first_name} {last_name}".strip()
```

#### Step 2: Register the utility

In your `configure.zcml`, add:

```xml
<utility
    factory=".title_generator.MyTitleGenerator"
    name="my_title_generator"
/>
```

#### Step 3: Activate your generator

To make your generator the default after installation, update the registry via GenericSetup by adding a `registry.xml` file in your profile:

```xml
<?xml version="1.0" encoding="utf-8"?>
<registry>
  <records
      interface="collective.person.controlpanel.interfaces.IPersonSettings"
      prefix="person">
    <value key="title_utility" purge="false">my_title_generator</value>
  </records>
</registry>
```


## License

The project is licensed under GPLv2.
