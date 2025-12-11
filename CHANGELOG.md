# Changelog

<!--
   You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst
-->

<!-- towncrier release notes start -->

## 1.0.0b4 (2025-12-11)


### Bug fixes:

- Fix handling of empty username field. @davisagli [#16](https://github.com/collective/collective.person/issues/16)

## 1.0.0b3 (2025-09-17)


### New features:

- Update the collective.contact_behaviors to 1.0.0b5. @iFlameing [#update](https://github.com/collective/collective.person/issues/update)

## 1.0.0b2 (2025-09-11)


### New features:

- Upgrade collective.contact_behaviors to version 1.0.0b4. @ericof [#13](https://github.com/collective/collective.person/issues/13)


### Bug fixes:

- Remove description from first name and last name fields.
  Add missing German translations. @davisagli [#11](https://github.com/collective/collective.person/issues/11)

## 1.0.0b1 (2025-09-09)


### Breaking changes:

- The behavior collective.person.person can only by applied to content types providing the collective.person.content.person.IPerson interface. @ericof 


### New features:

- Upgrade collective.contact_behaviors to version 1.0.0b3. @ericof [#5](https://github.com/collective/collective.person/issues/5)
- Add profile collective.person:catalog that adds contact_email, contact_phone and contact_website as metadata to the catalog. @ericof [#9](https://github.com/collective/collective.person/issues/9)


### Bug fixes:

- Ensure Title, sortable_title and SearchableText are properly indexed for Person content items. @ericof [#7](https://github.com/collective/collective.person/issues/7)


### Internal:

- Modernize packaging. @ericof [#3](https://github.com/collective/collective.person/issues/3)
- Fields IPersonData.description and IPersonData.role are not required anymore. @ericof [#6](https://github.com/collective/collective.person/issues/6)
- Add support to Python 3.12 and 3.13. @ericof 
- Drop support to Python 3.8 and 3.9. @ericof 
- Refactor GHA workflows. @ericof 
- Replace `pkg_resources` with `pkgutil`. @ericof 


### Documentation:

- Add example content demo profile. @ericof 

## 1.0.0a2 (2023-06-21)


### New features:

- Implement `Person` content type @ericof person
- Add pt_BR translation @ericof pt_BR
- Implement `collective.person.user` behavior @ericof user-behavior


## 1.0.0 (unreleased)
