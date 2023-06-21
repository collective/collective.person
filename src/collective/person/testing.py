from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING

import collective.person


class PersonLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.person)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.person:default")
        applyProfile(portal, "collective.person:testing")


FIXTURE = PersonLayer()


INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="PersonLayer:IntegrationTesting",
)


FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, PLONE_RESTAPI_DX_FUNCTIONAL_TESTING),
    name="PersonLayer:FunctionalTesting",
)
