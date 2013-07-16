from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.person',
      version=version,
      description="Portlets, content type, and behavior for persons as content.",
      long_description=open("README.md").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone portlet content',
      author='Sune Broendum Woeller',
      author_email='woeller@headnet.dk',
      url='http://plone.org',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.relationfield',
          'plone.z3cform',
          'zope.schema',
          'zope.interface',
          'zope.component',
          'plone.app.portlets',
          'collective.dexteritytextindexer',
          'plone.app.imagecropping',
          'plone.app.textfield',
          'plone.dexterity',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
